import json, csv, os, sys, time
from pprint import pprint
from urllib import urlopen


def make_music_csv():
	#global variables
	music_dicts = {}
	#gets the list of files in the a-z_music directory
	file_list = []
	for file_obj in os.walk("a-z_music/"):
		file_list = file_obj[2]
		break
	file_list = file_list[1:]

	apiKeys = ["JPGIYQEE2JFVVQFIZ", "EDTRTDL69QGI2KRW1", "LH8KBKRG97JTK8A2P"]

	keyCounter = 0
	currentKey = apiKeys[keyCounter]

	ens1="http://developer.echonest.com/api/v4/song/profile?api_key="
	ens2="&track_id=spotify:track:"
	ens3="&bucket=id:spotify&bucket=audio_summary"


	for music_file in file_list:
		#loads each json file

		with open("a-z_music/" + music_file) as data_file:
			data = json.load(data_file)
		
		dataItems  = data['tracks']['items']
		length = len(dataItems)

		tracks = {}



		
		for i in range(0,length):

			print "track index is is " + str(i)
			if i%19==0:
				print "i%19==0 and i is " +str(i) 
				print "switching api keys"
				keyCounter = (keyCounter + 1)%3
				currentKey=apiKeys[keyCounter]

			if i==49:
				print "sleeping for 60 secs ... zzz"
				time.sleep(60)

			currentTrack = dataItems[i]

			#print "currentTrack is "
			#pprint(currentTrack)

			#curTrack=currentTrack['name'].encode('utf-8')
			curTrack=currentTrack['id'].encode('utf-8')

			tracks[curTrack] = {'song_name':currentTrack['name'].encode('utf-8'),'album':currentTrack['album']['name'].encode('utf-8'), 'duration_ms':currentTrack['duration_ms'], 'explicit':currentTrack['explicit'], 'song_id': currentTrack['id'].encode('utf-8')}
			
			tracks[curTrack]['artists'] = []

			artistLength = len(currentTrack['artists'])
			
			tracks[curTrack]['artist_id']=currentTrack['artists'][0]['id'].encode('utf-8')

			artist_info=json.loads(urlopen("https://api.spotify.com/v1/artists/"+str(tracks[curTrack]['artist_id'])).read())
			
			# tracks[curTrack]['artist_popularity']=artist_info['popularity']
			tracks[curTrack]['num_of_artists']=artistLength 
			# tracks[curTrack]['num_artist_followers']=artist_info["followers"]["total"]

			enartist_url=ens1+currentKey+ens2+str(currentTrack['id'].encode('utf-8') )+ens3

			response_info=json.loads(urlopen(enartist_url).read())
			#print response_info
			audioShortcut = response_info['response']['songs'][0]['audio_summary']
			#print audioShortcut

			#audioDict['song_name'] = audioShortcut[5]
			#audioDict['artist_name'] = audioShortcut[2]
			tracks[curTrack]['danceability'] = audioShortcut['danceability']
			tracks[curTrack]['energy'] =  audioShortcut['energy']
			tracks[curTrack]['loudness'] = audioShortcut['loudness']
			tracks[curTrack]['speechiness'] = audioShortcut['speechiness']
			tracks[curTrack]['tempo'] = audioShortcut['tempo']
			tracks[curTrack]['song_title_en'] = response_info['response']['songs'][0]['title'].encode('utf-8')

			for artists in range (0, artistLength):
				#tracks[currentTrack['name'].encode('utf-8')]['artists'].append(currentTrack['artists'][artists]['name'].encode('utf-8'))
				tracks[curTrack]['artists'].append(currentTrack['artists'][artists]['name'].encode('utf-8'))


			print "ith or " +str(i) +" track is " + str(tracks[curTrack]['song_name']) 


					
		music_dicts[music_file] = tracks
		


	with open('finalish_song_list.csv', 'ab') as csvfile:
		fieldnames = ['song_name', 'song_id', 'artists', 'album', 'duration_ms', 'explicit', 'artist_id','num_of_artists', 'danceability','energy','loudness','speechiness','tempo','song_title_en']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for mdict in music_dicts:
			for key in music_dicts[mdict]:
				writer.writerow(music_dicts[mdict][key])
		

