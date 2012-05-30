#!/usr/bin/python

#A file sorter written in python

#To use this program, be inside the directory you're trying to sort
#when you call this program.

"""    ---BUGS---
Renaming to a file name that already exists then cancelling will
still change what the program thinks the file is called despite
not actually changing the file's name.

To-do
 Allow undos
 Add in viewing for txt/pdf
"""

import os
import sys

#I'll add more formats as I come across them
IMAGE_FORMATS = ['jpg', 'jpeg', 'bmp', 'png']
VIDEO_FORMATS = ['mp4', 'flv', 'avi', 'mkv', 'mov']
MUSIC_FORMATS = ['mp3']

FILE_ROOT = "/home/james/Stuff/"

IMAGE_DIR = FILE_ROOT + "Pictures/Wallpapers/"

VIDEO_DIR = FILE_ROOT + "Video/"
OTHER_VIDEO_DIR = VIDEO_DIR + "Other/"
TV_DIR = VIDEO_DIR + "TV\ Shows/"
MOVIE_DIR = VIDEO_DIR + "Movies/"

GIF_DIR = FILE_ROOT + "Pictures/gifs/"

MUSIC_DIR = FILE_ROOT + "Music/"
SOUND_DIR = MUSIC_DIR + "Other/"

#To use formatMap use: formatMap[fileType][command]
#                   or formatMap[fileType]['dir'][dir#]
#                   or formatMap['general']['m']
#o = open file, m = move file, O (capital O) = alternate open, r = rename
formatMap = {'image': {'o': 'feh -F "{0}"',
                       'dir': [IMAGE_DIR]},
             'video': {'o': 'mplayer "{0}"',
                       'dir': [VIDEO_DIR, OTHER_VIDEO_DIR,
                               TV_DIR, MOVIE_DIR]},
             'gif': {'o': 'animate "{0}"',
                     'O': 'chromium "{0}"',
                     'dir': [GIF_DIR]},
             'music': {'o': 'mpg123 "{0}"',
                       'dir': [MUSIC_DIR, SOUND_DIR]},
             'general': {'m': 'mv -i "{0}" "{1}"',
                         'r': 'mv -i "{0}" "{1}"' },
            }            

def is_type(file, extensions):
    """This function determines if the given file ends
    with any of the extensions given by the second argument
    """
    for extension in extensions:
        if file.endswith(extension):
            return True
    return False

def main():
    allFiles = os.listdir(os.getcwd())
    for file in allFiles:
        #Determine the file's type
        if is_type(file, IMAGE_FORMATS):
            fileType = 'image'
        elif file.endswith('gif'):
            fileType = 'gif'
        elif is_type(file, VIDEO_FORMATS):
            fileType = 'video'
        elif is_type(file, MUSIC_FORMATS):
            fileType = 'music'
        else:
            fileType = 'unknown'
        
        if fileType != 'unknown':
            originLoc = os.getcwd() + '/' + file
            targetDir = 0
            while True:
                targetLoc = formatMap[fileType]['dir'][targetDir]
                print("File:", file)
                print("Origin:", originLoc)
                print("Target:", targetLoc)

                c = input("Please enter a command: ")
                if c == 's': break #Skips this file
                elif c == 'q': sys.exit() #Quits
                elif c == 'p': #Switches directories
                    dirNum = len(formatMap[fileType]['dir'])
                    targetDir += 1
                    if targetDir == dirNum: targetDir = 0
                elif c == 'r': #Renames the file *PARTIALLY BROKEN* see top
                    newName = input("Enter a new name: ")
                    newLoc = os.getcwd() + '/' + newName
                    command = formatMap['general'][c].format(originLoc, newLoc)
                    os.system(command)
                    originLoc = str(newLoc)
                elif c == 'm': #Moves the file
                    command = formatMap['general'][c].format(originLoc,
                                                             targetLoc)
                    os.system(command)
                    break
                elif c in formatMap[fileType]:
                    command = formatMap[fileType][c].format(originLoc)
                    os.system(command)
                else:
                    print("Commands are: q, s, p, m, r, o, and maybe O")

main()
