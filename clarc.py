# This is a python script that can index text copied to the clipboard 
# into a dictionary. The keys may only contain alphanumeric characters, 
# and the values can only be plain text. Attempts to use other 
# characters in the key names will fail.

import sys
import os
import argparse
import re
import json

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

# Makes sure the directory is always the same.
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Arguments passed to the script from the command line.
parser = argparse.ArgumentParser(
    prog='Clipboard Archive',
    description='Archive your clipboard, or recover archived clipboards.')

parser.add_argument('-a', '--archive', type=str, metavar='<key>',
                    help='Archive your current clipboard with specified key.')

parser.add_argument('-c', '--copy', type=str, metavar='<key>',
                    help='Retrieve archived clipboard with specified key.')

args = parser.parse_args()

# The clipboard dictionary. It starts out empty.
clipboardArchive = {}
archiveFile = '.ARCHIVED_CLIPS.json'
# In case there isn't already an archived clips file, make one.
if not os.path.isfile(archiveFile):
    with open(archiveFile, 'w') as f:
        f.write('{ "foo":"bar" }')

root = tk.Tk()
root.withdraw()

# A regex that can check if a string contains any non-alphanumeric characters.
nonAlphaRegex = re.compile(r'\W')


# Saves the clipboardArchive to a specified file.
def saveArchive():
    with open(archiveFile, 'w') as f:
        archiveJson = json.dumps(clipboardArchive)
        f.write(archiveJson)


# Loads the clipboardArchive from a specified file.
def loadArchive():
    with open(archiveFile) as f:
        fileData = f.read()
        return json.loads(fileData)


# This determines if a given string contains only alphanumeric characters.
def alphaOnly(keyName):
    if nonAlphaRegex.search(keyName):
        return False
    return True


# Send the current value of the clipboard into clipboardArchive under a key.
# The key is only valid if all the characters are alphanumeric.
def archiveFromClipboard(keyName):
    try:
        textToArchive = root.clipboard_get()
    except tk.TclError:
        print('Clipboard is empty.')
        return
    if alphaOnly(keyName):
        print(f'Current clipboard saved to key \'{keyName}\'.')
        clipboardArchive[keyName] = textToArchive
    else:
        print('Invalid key. Keys must contain only letters,'
              ' numbers, and underscores.')


# Checks if a key is in the archive. If so, value is sent to clipboard.
def copyToClipboard(keyName):
    if keyName in clipboardArchive:
        root.clipboard_clear()
        root.clipboard_append(clipboardArchive[keyName])
        root.update()  # Makes the clipboard update (for some reason).
        print(f'{keyName} copied to clipboard.')
        return True
    else:
        print(f'There is no saved clipboard under the name \'{keyName}\'')
        return False


# Handles which functions to trigger based on args.
def clipCommands(a):
    didCommand = False
    if a.archive:
        archiveFromClipboard(a.archive)
        saveArchive()
        didCommand = True
    if a.copy:
        copyToClipboard(a.copy)
        didCommand = True
    if not didCommand:
        print('Invalid arguments. If you\'re having trouble try \'--help\'.')


# Loads the archive then interprets any commands.
clipboardArchive = loadArchive()
clipCommands(args)
