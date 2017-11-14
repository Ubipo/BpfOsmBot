# BpfOsmBot
Belgium Phone Format OSM Bot:
Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.

## How to use
Requires python 3, click and osmapi which can be installed trough:
```
λ pip install -r requirements.txt
```

### Main tool (for editing OSM objects):

If the tool finds an object with one or more 'too difficult' (refer to 'phoneFormat.py') to format phone numbers it skips the entire thing.

```
λ python BpfOsmBot.py --help
Usage: BpfOsmBot.py [OPTIONS] [IDSF] [CREDENTIALS]

  Belgium Phone Format OSM Bot:
  Converts phone and fax numbers of provided OSM object ids to the ITU-T 'E.164' standard.


  IDSF:               File containing ID's of objects to process. If not set,
                      ID's will be prompted for.

  CREDENTIALS:        File containing OSM username and password, one per line
                      like: '<username>:<password>'
                      If '--username' option is set, that user will be used.

Options:
  --osm-type [node|way|relation]  Which object type to scan.
  --tag TEXT                      Which tags to correct. Overrides default of:
                                  phone contact:phone fax contact:fax
  --upload                        If set, the script uploads data to the OSM
                                  server.
  --url TEXT                      OSM API server URL. Default is 'https://api.
                                  master.apis.dev.openstreetmap.org'
  --username TEXT                 Used to login to the OSM API, edits will be
                                  displayed under this name.
  --password TEXT                 Password of said user.
  --comment TEXT                  Changeset comment. Default is 'BPF_BOT
                                  Phone/Fax number correction'
  --verbose                       If set, logs debug messages to the console.
  --unattended                    If set, defaults are used in place of user
                                  input.
  --log-level [debug|info|warning|error|critical]
                                  Console logging level, doesn't affect file
                                  log. Overrides '--verbose' flag. Default is
                                  info.
  --help                          Show this message and exit.
```

### Tester tool (for testing the phone format script):
```
λ python formatTester.py "<Belgian phone/fax number to format>"
```
