import requests
import json
from pyDes import *
import base64
from pydub import AudioSegment
import os

url = "https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids="

def format(string):
    return string.encode().decode('unicode-escape').replace("&quot;","'").replace("&amp;", "&").replace("&#039;", "'")

def jiosaavndl(inpurl):
        if(inpurl > ''):
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
                open(filename, 'wb').write(song.content)
                finalname = os.path.splitext(filename)[0]
                AudioSegment.from_file(filename).export(finalname + ".mp3", format="mp3", bitrate="320k")
                return