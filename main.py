#! /usr/bin/python3
import re
import subprocess
import sys
import os
import glob
import json

file = "/home/rishabh/Projects/py/shows.json"


# def createFile():
#     try:
#         f = open("shows.json", "a")
#         f.write("[]")
#         f.close()
#     except Exception as e:
#         raise e
#
#
# createFile()

shows = []
selectedShow = {}
selectedShowIndex = None


def addNewShow():
    name = input("Enter name: ")
    epi = input("Enter epi: ")
    dir = os.getcwd() + "/"
    show = {
        "name": name,
        "epi": int(epi),
        "dir": dir
    }
    with open(file, 'r+') as f:
        data = json.load(f)
        data.append(show)
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
    selectShow()


def readJson(file):
    f = open(file)
    data = json.load(f)
    shows.clear()
    for i in data:
        shows.append(i)
    f.close()


def printShows(shows):
    for i, show in enumerate(shows):
        print(i, show['name'], "epi:", show['epi'])
    print(i+1, "Add new show")


def selectShow():
    global selectedShowIndex
    global selectedShow
    readJson(file)
    printShows(shows)
    selectedShowIndex = input("Select show from the list: ")
    if int(selectedShowIndex) == len(shows):
        addNewShow()
    else:
        selectedShow = shows[int(selectedShowIndex)]
        print(selectedShow['name'])


selectShow()


def editJson(file):
    with open(file, 'r+') as f:
        data = json.load(f)
        data[int(selectedShowIndex)]['epi'] += 1  # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part


# play video
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def getCurrentFile(selectedShow, next=False):
    if not next:
        selectedShow['dir'] = re.sub('([\[\]])', '[\\1]', selectedShow['dir'])
    list_of_files = []
    list_of_files.extend(
        filter(os.path.isfile, glob.glob(selectedShow['dir'] + '*.mkv')))
    list_of_files.extend(
        filter(os.path.isfile, glob.glob(selectedShow['dir'] + '*.mp4')))
    list_of_files = sorted(list_of_files)
    return list_of_files[selectedShow['epi']-1]


open_file(getCurrentFile(selectedShow))


def playNext():
    nextEpiOrNa = input("Play next epi (y,n)? ")
    if nextEpiOrNa == "y":
        selectedShow['epi'] += 1
        open_file(getCurrentFile(selectedShow, True))
        incEpi()
    else:
        print("Bye")


def incEpi():
    incEpiOrNa = input("Do u want to increase the epi no (y,n): ")
    if incEpiOrNa == "y":
        editJson(file)
        print(selectedShow['name'], ":", selectedShow['epi'] + 1)
        playNext()
    else:
        print("Bye")


incEpi()
