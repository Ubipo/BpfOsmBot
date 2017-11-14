'''
=== phoneFormat.py ===

Belgian Phone number Formatter
Formats belgian phone numbers from given id('s) to the ITU-T 'E.164' standard
argument: phone #
returns: string, either:
  'error' on too difficult/unknown of a number or
  formatted number
'''

def belgium(raw):
  #-------------------
  # Declarations
  clean = ''
  norm = ''
  sliced = []
  fomatted = ''
  error = False

  '''
  'Safe' area codes, excluding:

  '800' - Toll free service - !! Area code '80' is valid
  '70' - Premium rate services
  '77' - Machine to machine communication
  '78' - National rate services
  '90' - Premium numbers 
  '''
  safeCodes = ['10', '11', '12', '13', '14', '15', '16', '19', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '63', '64', '65', '67', '68', '69', '71', '80', '81', '82', '83', '84', '85', '86', '87', '89']

  shortCodes = ['2', '3', '4', '9']

  # First 2 digits of 
  mobCodes = ['46', '47', '48', '49']

  #-------------------

  # Get only numbers and remove preceding zero's
  precZero = True
  for c in raw:
    if c.isdigit():
      if not (c == '0' and precZero):
        clean+=str(c)
        precZero = False

  # Check if there's a Belgian int country code in fornt. If so, remove
  if len(clean) >= 9 and clean[:2] == '32':
    clean = clean[2:]

  # Again remove preceding zero's
  precZero = True
  for c in clean:
    if not (c == '0' and precZero):
      norm+=str(c)
      precZero = False

  # Check if area code is a short code <x xxx xx xx> (or is a Liège number) or long code <(xxx/xx) xx xx xx> and
  # extract area code and first part of subscriber number
  if norm[:1] in shortCodes and len(norm) == 8:
    sliced.append(norm[:-7])
    sliced.append(norm[-7:-4])
  else:
    sliced.append(norm[:-6])
    sliced.append(norm[-6:-4])

  # Extract the last two parts of the subscriber number
  sliced.append(norm[-4:-2])
  sliced.append(norm[-2:])

  # Check if the number has a known safe area code
  if sliced[0] in safeCodes or sliced[0] in shortCodes or sliced[0][:-1] in mobCodes:
    formatted = '+32 ' + sliced[0] + ' ' + sliced[1] + ' ' + sliced[2] + ' ' + sliced[3]
  else:
    error = True

  if error:
    return('error')
  else:
    return(formatted)