#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import random
import string

# directly implements randomGenWords.py
def generate():
    count = nameCheck = charPlace = modeCheck = 0
    letters = string.ascii_lowercase + string.ascii_uppercase
    fileText = ""
    defaultName = "randomGenWords"
    defaultWords = "500000"

    # User Selects mode for file. Will either extend the overall file or overwrite it.
    # Note: Append is mostly for testing fuse in that one can add onto file in the base directory
    #       and check on relink.
    mode = input("Do you want to Append ('A') or Overwrite ('W') a file: ")
    while (modeCheck < 1):
        if (mode == "" or mode == 'W' or mode == 'w'):
            mode = 'w'
            modeCheck += 1
        elif (mode == 'A' or mode == 'a'):
            mode = 'a'
            modeCheck += 1
        else:
            mode = input("This is not a valid input. Please use proper value: ")

    # User can include a directory in the name to create the file there.
    #   ex: Directory/filename will create the file in the subsequent directory.
    filename = input("Please enter file name: ")
    while (nameCheck < 1):
        if (filename == ""):
            filename = defaultName
            nameCheck += 1
        # Prevents files being created in directories from being named nothing
        # or starting with numbers
        elif (filename.find('/') > 0):
            if ('/' == filename[-1]):
                filename += defaultName
                nameCheck += 1
            else:
                for c in filename:
                    if (c != '/'):
                        charPlace += 1
                        break
                if (filename[charPlace:].isnumeric() or filename[charPlace+1].isnumeric()):
                    charPlace = 0
                    filename = input("This is an improper file name. Please give the file a proper name: ")
        elif (filename[0:].isnumeric()):
            filename = input("This is an improper file name. Please give the file a proper name: ")
        else:
            nameCheck += 1  

    # The current cap, 500000 words, takes around 5-8 seconds to create.
    # Note when running passthrough.py:
    #           Time to make file at max words is about 3 times longer
    numWords = input("Please enter the amount of words (less than 500000): ")
    while (not numWords.isnumeric() or int(numWords) > 500000):
        if (numWords == ""):
            numWords = defaultWords
        else:
            words = input("This is an invalid input. Please enter a proper value: ")

    # This will write over other files with the same name
    # Note when running passthrough.py:
    #           Debug messages seem to be called every 10000 characters or so.
    with open ('mp/' + filename + '.txt', mode) as f:
        while (count < int(numWords)):
            wordLen = random.randint(1,10)    # Gives words different lengths
            word = ''.join(random.choice(letters) for i in range (wordLen)) + ' '
            fileText += word
            count += 1
        fileText += '\n'
        f.write(fileText)       

# edits a file in basedir to prevent its
# checksum from being updated in the dictionary
def corrupt():
    filename = None
    while True:
        print("Choose a .txt file to corrupt: (input without .txt)")
        os.system('ls basedir')

        filename = input("> ")
        if (not os.path.exists('basedir/' + filename + '.txt')):
            print("Invalid filename.\n")
        else:
            break
                  
    with open ('basedir/' + filename + '.txt', "a") as f:
        f.write("i'm a bad file!")

if not os.path.exists('basedir'): os.mkdir('basedir')
if not os.path.exists('mp'): os.mkdir('mp')

os.popen('konsole')
os.popen('konsole -e python passthrough.py basedir mp')

loop = True
while (loop):
    print("FUSE Group Project testing commands")
    print("[1] Delete .md5_hashes")
    print("[2] Generate random file")
    print("[3] Corrupt a file")
    print("[0] Exit")
    cmd = input("> ")
    
    if (cmd == '1'):
        os.system('rm basedir/.md5_hashes')
        os.system('clear')
        print(".md5_hashes has been deleted.\n")
    elif (cmd == '2'):
        generate()
        os.system('clear')
        print("Random file has been generated.\n")
    elif (cmd == '3'):
        corrupt()
        os.system('clear')
        print("Selected file has been corrupted.\n")
    elif (cmd == '0'):
        loop = False
    else:
        os.system('clear')
        print("Invalid command.\n")

os.system('clear')
print("You may close this window now.")
