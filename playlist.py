# -*- coding: utf-8 -*-

import spotipy
import sys
import datetime
import keys as keys

from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=keys.client_id,
                                                      client_secret=keys.client_secret)
spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


username = keys.spot_username  # your username (not an email address)

createnewplaylist = True  # Set this to true to create a new playlist with the name below; set this to false to use an already created playlist, and follow instructions below
newplaylistname = 'Top'

date = str(datetime.datetime.today().strftime('%m-%d-%y'))
description = 'Automatically generated ' + date + 'beep boop'


# If using an already existing playlist, go to Spotify and right click on a playlist and select "Copy Spotify URI". Paste the value below, keeping only the numbers at the end of the URI
oldplaylistID = '3uEcg6o2uf2ijoyeRj3zLiF'

dataFile = "output.txt"
delim = ' - '  # charecters between song title and artist in your data file; make sure this is not something that could be present in the song title or artist name

my_client_id = keys.client_id
my_client_secret = keys.client_secret
######
######


import sys
import spotipy
import spotipy.util as util
import requests

scope = 'user-library-read playlist-modify-public playlist-modify-private'

data = open(dataFile).readlines()
#period = open(dataFile).readline().rstrip()
#print(period)
token = util.prompt_for_user_token(username, scope, client_id=my_client_id,
                                   client_secret=my_client_secret, redirect_uri='http://localhost:8888/callback')
myAuth = "Bearer " + token

notfound = []
b = 0
if token:
    sp = spotipy.Spotify(auth=token)

    if createnewplaylist:
        r = sp.user_playlist_create(username, newplaylistname, False, description)

        playlistID = r['id']
        sp.user_playlist_change_details(username, playlistID, newplaylistname, False, False, description)
        #sp.user_playlist_change_details(username, playlistID, newplaylistname, description)
        #sp.user_playlist_change_details(username, playlistID, name=newplaylistname, public=None, collaborative=None, description=description)


    else:
        playlistID = oldplaylistID

    for line in data:
        l = line.split(delim)
        # If you have any characters after your track title before your delimiter, add [:-1] (where 1 is equal to the number of additional characters)
        trackTitle = l[0]
        # [:-1] removes the newline at the end of every line. Make this [:-2] if you also have a space at the end of each line
        artist = l[1][:-1]

        #art = artist.replace('e','e')
        #trk = trackTitle.replace('®','')
        art = artist
        trk = trackTitle
        q = '{} {}'.format(art, trk)


        r = sp.search(q=q)

        a=0

        for track in r['tracks']['items']:
            a+=1
            b+=1

            artists =[r['tracks']['items'][0]['name']]

            track_id = [r['tracks']['items'][0]['uri']]
            sp.user_playlist_add_tracks(username, playlistID, track_id)

            output = str("Added " + trk + " by " + art)
            print(output)

            if a == 1:
                break
    if b == 30:
            print("Added 30 songs")

    else:
            print("Missing " + str(30-b) + " song(s)")

else:
    print("exit")
