import phoneFormat
import osmapi
import logging
import argparse
import click

'''
=== BpfOsmBot.py ===

Belgium Phone Format OSM Bot:
Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.

Commented lines marked with '$' are for r/w behaviour 
'''

# =======================
# > Variables ===========
# =======================

# Tag names the bot is trying to fix
defaultTagsNames = ['phone', 'contact:phone', 'fax', 'contact:fax']
defaultUrl = 'https://api06.dev.openstreetmap.org'
defaultComment = 'BPF_BOT Phone/Fax number correction'
logFile = 'BpfOsmBot.log'


# =======================
# > Declarations ========
# =======================

log = None

# Logger
def startLogger(clLevel):
  global log

  clLevelNum = getattr(logging, clLevel.upper(), None)

  formatCl = logging.Formatter(fmt='{levelname: <9} {message}', style='{')
  formatFile = logging.Formatter(fmt='{asctime: <24} {levelname: <9} {message}', style='{')

  log = logging.getLogger('BpfOsmBot')
  log.setLevel(logging.DEBUG)

  # Create command line and file handlers
  ch = logging.StreamHandler()
  ch.setLevel(clLevelNum)
  ch.setFormatter(formatCl)

  fh = logging.FileHandler(logFile, mode='a')
  fh.setLevel(logging.DEBUG)
  fh.setFormatter(formatFile)

  log.addHandler(ch)
  log.addHandler(fh)

# Actual tag editor
def fixObject(osmObject, tagNames):
  # Create return dictionary
  returnDic = {'tagsChanged': False, 'formatError': False, 'object': ''}

  # Scan all tags of object for tags matching 'tagNames'
  tags = osmObject['tag']
  for tagName in tagNames:
    if tags.get(tagName, False):
      # Format the tag
      formatted = phoneFormat.belgium(tags[tagName])
      if formatted != 'error':
        log.info('Updated '  + tagName + ' from ' + tags[tagName] + ' to ' + formatted)
        # Formatting successful, change the tag
        returnDic['tagsChanged'] = True
        tags[tagName] = formatted
      else:
        # Formatting error, leave tag unchanged
        returnDic['formatError'] = True
        log.error('Error parsing ' + tagName + ': ' + tags[tagName])

  # Replace osmObject's tags with new ones
  osmObject['tag'] = tags

  # Return
  returnDic['object'] = osmObject
  return returnDic

# Removes personal tags from the object added by previous editor
def cleanObject(osmObject):
  del osmObject['changeset'] # automatically added
  del osmObject['timestamp'] # Idem
  del osmObject['user'] # Idem
  del osmObject['uid'] # Idem

  return osmObject

# Uses OSM API to retrieve an object
def getObject(api, osmType, osmId):
  if osmType == 'node':
    return api.NodeGet(osmId)
  elif osmType == 'way':
    return api.WayGet(osmId)
  elif osmType == 'relation':
    return api.RelationGet(osmId)
  else:
    log.exception('Internal type error.')
    raise SystemExit(0)

# Uses OSM API to update an object
def updateObject(api, osmType, osmObject):
  if osmType == 'node':
    api.NodeUpdate(osmObject)
  elif osmType == 'way':
    api.WayUpdate(osmObject)
  elif osmType == 'relation':
    api.RelationUpdate(osmObject)
  else:
    log.exception('Internal type error.')
    raise SystemExit(0)


# =======================
# > START ===============
# =======================

# === Click ===
@click.command()

# File arguments
@click.argument('idsf', required=False, type=click.File('r'))
@click.argument('credentials', required=False, type=click.File('r'))

# Options
@click.option('--osm-type', type=click.Choice(['node', 'way', 'relation']), default='node', prompt='> Which OSM object type to edit?', help='Which object type to scan.')
@click.option('--tag', multiple=True, help='Which tags to correct. Overrides default of: '+' '.join(defaultTagsNames), default=defaultTagsNames)
@click.option('--upload', is_flag=True, prompt='> Upload data to OSM database? If no a simulation is run', help='If set, the script uploads data to the OSM server.')
@click.option('--url', help='OSM API server URL. Default is \''+defaultUrl+'\'')
@click.option('--username', help='Used to login to the OSM API, edits will be displayed under this name.')
@click.option('--password', help='Password of said user.')
@click.option('--comment', help='Changeset comment. Default is \''+defaultComment+'\'', default=defaultComment)
@click.option('--verbose', is_flag=True, help='If set, logs debug messages to the console.')
@click.option('--unattended', is_flag=True, help='If set, defaults are used in place of user input.')
@click.option('--log-level', type=click.Choice(['debug', 'info', 'warning', 'error', 'critical']),  default='info', help='Console logging level, doesn\'t affect file log. Overrides \'--verbose\' flag. Default is info.')


def main(idsf, credentials, osm_type, tag, upload, url, username, password, comment, unattended, verbose, log_level):
  """
  \b
  Belgium Phone Format OSM Bot:
  Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.

  \b
  \b
  IDSF:               File containing ID\'s of objects to process. If not set,
                      ID's will be prompted for.
  \b
  CREDENTIALS:        File containing OSM username and password, one per line
                      like: '<username>:<password>'
                      If '--username' option is set, that user will be used.

  """

  # === Setup ===

  # Start the logger
  print('Logging to \'' + logFile + '\'...')
  if verbose:
    startLogger('debug')
  else:
    startLogger(log_level)

  # Additional questions for unfilled values
  if upload:
    log.warning('Upload is ON')
    # Check if URL is provided
    if not url:
      url = click.prompt('> Enter OSM API server URL', default=defaultUrl)
    # Check if username and password is provided
    if not (username and password):
      # Check if a credentials file is provided
      if credentials:
        # Extract credentials
        credsList = []
        for line in credentials: 
          credsList.append(line.strip().split(':'))
        if len(credsList) > 1 and not unattended:
          while not password:
            username = click.prompt('> Enter username to from \''+credentials.name+'\', edits will be displayed under this name')
            # Find provided username
            found = False
            for creds in credsList:
              if creds[0] == username:
                found = True
                if not len(creds) < 2:
                  username = creds[0]
                  password = creds[1]
                else:
                  print('There\'s a problem with that username.')
                  if not click.confirm('> Try again?'):
                    username = click.prompt('> Enter username to log into OSM API, edits will be displayed under this name')
                    password = click.prompt('> Enter password of said user', hide_input=True)
                    break
            if not found:
              log.error('Username not found, try again.')
        else:
          creds = credsList[0]
          if not len(creds) < 2:
            username = creds[0]
            password = creds[1]
          elif unattended:
            log.critical('Problem with credentials.')
            raise SystemExit(0)
          else:
            print('There\'s a problem with the credentials in \''+credentials.name+'\'.')
            username = click.prompt('> Enter username to log into OSM API, edits will be displayed under this name')
            password = click.prompt('> Enter password of said user', hide_input=True)
      else:
        username = click.prompt('> Enter username to log into OSM API, edits will be displayed under this name')
        password = click.prompt('> Enter password of said user',  hide_input=True)

    log.info('Credentials are: \'' + username + ':' + '*'*len(password) + '\'')
    api = osmapi.OsmApi(api = url, username = username, password = password, changesetauto=True, changesetautotags={"comment": comment, "bot": "yes"}, changesetautosize=200, changesetautomulti=1)

  else:
    # If we're not uploading changes, don't provide the OSM API with a username/password
    api = osmapi.OsmApi()

  # Get the IDS of objects to edit
  ids = []
  if idsf:
    for line in idsf: 
      ids.append(line.strip())
  else:
    while True:
      ids.append(click.prompt('> Enter OSM object ID to fix'))
      if not click.confirm('> Add another?'):
        break

  log.debug('Type: ' + osm_type)
  log.debug('Ids: ' + ' '.join(ids))
  log.debug('Tags: ' + ' '.join(tag))

  # === Main loop ===
  for objectId in ids:
    log.info('Processing id: \'' + objectId + '\'...')
    objectOld = cleanObject(getObject(api, osm_type, objectId))
    fixData = fixObject(objectOld, tag)
    objectNew = fixData['object']
    log.debug('Raw objects: \n Old: ' + str(objectOld) + '\n New: ' + str(objectNew) + '\'')
    if not fixData['formatError'] and fixData['tagsChanged']:
      if upload:
        updateObject(api, osm_type, objectNew)
      else:
        log.info(objectNew)
    elif not fixData['formatError'] and not fixData['tagsChanged']:
      log.info('Didn\'t update, nothing to change.')
    elif fixData['formatError']:
      log.error('Didn\'t update, difficult or no number detected.')
    else:
      log.error('Unknown error.')

  # === Exit ===

  log.info('Done! Exiting...')

if __name__ == '__main__':
    main()

