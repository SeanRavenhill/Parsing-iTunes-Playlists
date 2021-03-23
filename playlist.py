'''
playlist.py

Description: Playing with iTunes Playlists.

Original Author: Mahesh Venkitachalam
Website: electronut.in

Follow along course project from:
Python Playground - Geeky Projects for
the Curious Programmer.

Copyright © 2016 by Mahesh Venkitachalam.

Chapter 1: Parsing iTunes Playlists

Revisions to Code made by: Sean Ravenhill
Revisions marked by opening and closing *** in comments.
'''


import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np

# Below function finds duplicates of tracks in an iTunes library.
# Writes a text file reporting the duplications.

def findDuplicates(fileName):
    print('Finding duplicate tracks in %s...' %fileName)
    # read in a playlist
    # *** Original code - plist = plistlib.readPlist(fileName)
    # Reverted to .readPlist as method depracated error thrown.
    # (open(fileName, 'rb')) arguments required to read files
    # as binary object. ***
    plist = plistlib.load(open(fileName, 'rb'))
    # get the tracks from the Tracks dictionary
    tracks = plist['Tracks']
    # create a track name dictionary
    trackNames = {}
    # iterate through the Tracks
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            # look for existing entries
            if name in trackNames:
                # if a name and duration match, increment the count
                # round the track length to the nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                # add dictionary entry as tuple (duration, count)
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass

    # store duplicates as (name, count) tuples
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            # *** Swapped around k, v[1] from original code. ***
            dups.append((k, v[1]))
    # save duplicates to a file
    if len(dups) > 0:
        print('Found %d duplicates. Track names saved to duplicates.txt' %len(dups))
    else:
        print('No duplicate tracks found!')
    f = open('duplicates.txt', 'w')
    for val in dups:
        # *** Edits to how the string is rendered and read ***
        f.write('%s [%d]\n' %(val[0], val[1]))
    f.close()

# Below function finds common tracks between playlist files.
# Writes a text file reporting the common tracks.

def findCommonTracks(fileNames):
    # a list of sets of track track names
    trackNameSets = []
    for fileName in fileNames:
        # create a new set
        trackNames = set()
        # read in playlist
        # *** Original code - plist = plistlib.readPlist(fileName)
        # Reverted to .readPlist as method depracated error thrown.
        # (open(fileName, 'rb')) arguments required to read files
        # as binary object. ***
        plist = plistlib.load(open(fileName, 'rb'))
        # get the tracks
        tracks = plist['Tracks']
        # iterate through the tracks
        for trackId, track in tracks.items():
            try:
                # add the track name to a set
                trackNames.add(track['Name'])
            except:
                # ignore
                pass
        # add to list
        trackNameSets.append(trackNames)
    # get the set of common tracks
    commonTracks = set.intersection(*trackNameSets)
    # write to file:
    if len(commonTracks) > 0:
        # *** Had to add, 'wb' write binary to this line ***
        f = open('commom tracks.txt', 'wb')
        for val in commonTracks:
            s = '%s\n' %val
            f.write(s.encode('UTF-8'))
        f.close()
        print('%d common tracks found.\nTrack names written to common tracks.txt' %len(commonTracks))
    else:
        print('No common tracks!')

# Below function below gathers and renders out Data from playlist.

def plotStats(fileName):
    # read in a playlist
    # *** Original code - plist = plistlib.readPlist(fileName)
    # Reverted to .readPlist as method depracated error thrown.
    # (open(fileName, 'rb')) arguments required to read files
    # as binary object. ***
    plist = plistlib.load(open(fileName, 'rb'))
    # get the tracks from the playlist
    tracks = plist['Tracks']
    # create lists of song rating and track duractions
    ratings = []
    durations = []
    # iterate through the tracks
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            # ignore
            pass
    # ensure that valid data was collected:
    if ratings == [] or durations == []:
        print('No valid Album Rating/Total Time data in %s.' %fileName)
        return

    # scatter plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2, 1, 1)
    pyplot.plot(x, y, 'o')
    pyplot.axis([1, 1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Track Rating')

    # histogram plot
    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Count')

    #show plot
    pyplot.show()

# gather our code in a main() function
def main():
    # create parser
    descStr = '''
    This program analyzes plalist files (.xml) exported from iTunes.
    '''
    parser = argparse.ArgumentParser(description=descStr)

    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        # find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        # *** Edit to printed string... just for kicks ;p ***
        print('These are not the droids... ummm... tracks.... the tracks you are looking for.')

# main method
if __name__ == '__main__':
    main()
