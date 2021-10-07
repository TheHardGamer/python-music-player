import requests
import json
from pyDes import *
import base64
from pydub import AudioSegment
import os
import shutil

url = "https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids="
albumurl = "https://www.jiosaavn.com/api.php?__call=content.getAlbumDetails&_format=json&cc=in&_marker=0%3F_marker%3D0&albumid="

def format(string):
    return string.encode().decode('unicode-escape').replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")

def jiosaavndl(inpurl):
	if(inpurl > ''):
		if "/song/" in inpurl:
			res = requests.get(inpurl, data=[('bitrate', '320')])
			pid = res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
			finalurl = url + pid
			encid = requests.get(finalurl).text.encode().decode('unicode-escape')
			encid = json.loads(encid)
			jsondata = encid[pid]
			jsondata['media_url'] = jsondata['encrypted_media_url']
			jsondata['song'] = format(jsondata['song'])
			des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
			enc_url = base64.b64decode(jsondata['encrypted_media_url'].strip())
			dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
			dec_url = dec_url.replace("_96.mp4", "_320.mp4")
			filename = jsondata['song'] + ".m4a"
			song = requests.get(dec_url, allow_redirects=True, timeout=5)
			if(os.path.exists(jsondata['song'])):
				shutil.rmtree(jsondata['song'])
			os.mkdir(jsondata['song'])
			foldername = jsondata['song'] + '/' + filename
			open(foldername, 'wb').write(song.content)
			finalname = os.path.splitext(filename)[0]
			AudioSegment.from_file(foldername).export(jsondata['song'] + '/' + finalname + ".mp3", format="mp3", bitrate="320k")
			os.remove(jsondata['song'] + '/' + filename)
		else:	
			res = requests.get(inpurl)
			album_id = res.text.split('"album_id":"')[1].split('"')[0]
			response = requests.get(albumurl+album_id)
			songs_json = response.text.encode().decode('unicode-escape')
			songs_json = json.loads(songs_json)
			if(os.path.exists(songs_json['name'])):
				shutil.rmtree(songs_json['name'])
			os.mkdir(songs_json['name'])
			for song in songs_json['songs']:
				song['media_url'] = song['encrypted_media_url']
				song['song'] = format(song['song'])
				des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",pad=None, padmode=PAD_PKCS5)
				enc_url = base64.b64decode(song['encrypted_media_url'].strip())
				dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
				dec_url = dec_url.replace("_96.mp4", "_320.mp4")
				filename = song['song'] + ".m4a"
				song = requests.get(dec_url, allow_redirects=True, timeout=5)
				open(songs_json['name'] + '/' + filename, 'wb').write(song.content)
				finalname = os.path.splitext(filename)[0]
				AudioSegment.from_file(songs_json['name'] + '/' + filename).export(songs_json['name'] + '/' + finalname + ".mp3", format="mp3", bitrate="320k")
				os.remove(songs_json['name'] + '/' + filename)