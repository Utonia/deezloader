#!/usr/bin/python3
import os
import json
import mutagen
import spotipy
import requests
from tqdm import tqdm
from Crypto.Hash import MD5
from bs4 import BeautifulSoup
import spotipy.oauth2 as oauth2
from mutagen.id3 import ID3, APIC
from mutagen.easyid3 import EasyID3
from binascii import a2b_hex, b2a_hex
from Crypto.Cipher import AES, Blowfish
req = requests.Session()
localdir = os.getcwd()
def generate_token():
    credentials = oauth2.SpotifyClientCredentials(client_id="4fe3fecfe5334023a1472516cc99d805", client_secret="0f02b7c483c04257984695007a4a8d5c")
    token = credentials.get_access_token()
    return token
token = generate_token()
spo = spotipy.Spotify(auth=token)
header = {
          "Accept-Language": "en-US,en;q=0.5"
}
params = {
          "api_version": "1.0",
          "api_token": "null",
          "input": "3",
          "method": "deezer.getUserData"
}
class TrackNotFound(Exception):
      def __init__(self, message):
          super().__init__(message)
class AlbumNotFound(Exception):
      def __init__(self, message):
          super().__init__(message)
class InvalidLink(Exception):
      def __init__(self, message):
          super().__init__(message)
class BadCredentials(Exception):
      def __init__(self, message):
          super().__init__(message)
class QuotaExceeded(Exception):
      def __init__(self, message):
          super().__init__(message)
class Login:
      def __init__(self, mail, password):
          check = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results']['checkFormLogin']
          post_data = {
                       "type": "login",
                       "mail": mail,
                       "password": password,
                       "checkFormLogin": check
          }
          sign = req.post("https://www.deezer.com/ajax/action.php", post_data).text
          if "success" in sign:
           print("Success, you are in")
          else:
              raise BadCredentials("Invalid password or username")
      def download(self, track, location):
          song = {}
          ids = track.split("/")[-1]
          name = ids + ".mp3"
          def login():
              try:
                 token = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results']['checkForm']
              except:
                 token = json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", params).text)['results']['checkForm']
              data = {
                      "api_version": "1.0",
                      "input": "3",
                      "api_token": token,
                      "method": "song.getData"
              }
              param = json.dumps({"sng_id": ids})
              try:
                 return json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", param, params=data).text)
              except:
                 return json.loads(req.post("http://www.deezer.com/ajax/gw-light.php", param, params=data).text)
          def md5hex(data):
              h = MD5.new()
              h.update(data)
              return b2a_hex(h.digest())
          def genurl():
              data = b"\xa4".join(a.encode() for a in [song['md5'], "1", str(ids), str(song['media_version'])])
              data = b"\xa4".join([md5hex(data), data])+ b"\xa4"
              if len(data) % 16:
               data += b"\x00" * (16 - len(data) % 16)
              c = AES.new("jo6aey6haid2Teih", AES.MODE_ECB)
              c = b2a_hex(c.encrypt(data)).decode()
              return "https://e-cdns-proxy-8.dzcdn.net/mobile/1/" + c
          def calcbfkey(songid):
              h = md5hex(b"%d" % int(songid))
              key = b"g4el58wc0zvf9na1"
              return "".join(chr(h[i] ^ h[i + 16] ^ key[i]) for i in range(16))
          def blowfishDecrypt(data, key):
              c = Blowfish.new(key, Blowfish.MODE_CBC, a2b_hex("0001020304050607"))
              return c.decrypt(data)
          def decryptfile(fh, key, fo):
              i = 0
              for data in fh:
                  if not data:
                   break
                  if (i % 3) == 0 and len(data) == 2048:
                   data = blowfishDecrypt(data, key)
                  fo.write(data)
                  i += 1
          infos = login()
          song['md5'] = infos['results']['MD5_ORIGIN']
          song['media_version'] = infos['results']['MEDIA_VERSION']
          try:
             fh = requests.get(genurl())
          except:
             fh = requests.get(genurl())
          if len(fh.content) == 0:
           raise TrackNotFound("")
          open(location + name, "wb").write(fh.content)
          fo = open(location + name, "wb")
          decryptfile(fh.iter_content(2048), calcbfkey(ids), fo)
      def download_trackdee(self, URL, output=localdir + "/Songs/", check=True):
          if output == localdir + "/Songs":
           if not os.path.isdir("Songs"):
            os.makedirs("Songs")
          array = []
          music = []
          artist = []
          album = []
          tracknum = []
          discnum = []
          year = []
          genre = []
          ar_album = []
          if "?" in URL:
           URL,a = URL.split("?")
          URL = "http://www.deezer.com/track/" + URL.split("/")[-1]
          try: 
             url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
          except:
             url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             if url['error']['message'] == "no data" or url['error']['message'] == "Invalid query":
              raise InvalidLink("Invalid link ;)")
          except KeyError:
             None
          try:
             url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
          except:
             url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
          try:
             if url1['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:   
             image = url['album']['cover_xl'].replace("1000", "1200")   
          except:
             try:
                image = requests.get(URL).text
             except:
                image = requests.get(URL).text
             image = BeautifulSoup(image, "html.parser").find("img", class_="img_main").get("src").replace("120", "1200")
          music.append(url['title'])
          for a in url['contributors']:
              array.append(a['name'])
          if len(array) > 1:
           for a in array:
               for b in range(len(array)):
                   try:
                      if a in array[b] and a != array[b]:
                       del array[b]
                   except IndexError:
                      break
          artist.append(", ".join(array))
          album.append(url['album']['title'])
          tracknum.append(url['track_position'])
          discnum.append(url['disk_number'])
          year.append(url['album']['release_date'])
          song = music[0] + " - " + artist[0]
          try:
             if url1['error']['message'] == "no data":
              raise TrackNotFound("Track not found: " + song)
          except KeyError:
             None
          try:
             for a in url1['genres']['data']:
                 genre.append(a['name'])
          except KeyError:
             None
          for a in url1['contributors']:
              if a['role'] == "Main":
               ar_album.append(a['name'])
          dir = str(output) + "/" + artist[0].replace("/", "") + "/"
          try:
             if not os.path.isdir(dir):
              os.makedirs(dir)
          except:
             None
          name = artist[0].replace("/", "") + " " + music[0].replace("/", "") + ".mp3"
          if os.path.isfile(dir + name):
           if check == False:
            return dir + name
           ans = input("Song already exist do you want to redownload it?(y or n):")
           if not ans == "y":
            return
          print("\nDownloading:" + song)
          try:
             self.download(URL, dir)
          except TrackNotFound:
             try:
                url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace("#", "")).text)
             except:
                url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace("#", "")).text)
             try:
                if url['error']['message'] == "Quota limit exceeded":
                 raise QuotaExceeded("Too much requests limit yourself")
             except KeyError:
                None
             try:
                for a in range(url['total'] + 1):
                    if url['data'][a]['title'] == music[0] or url['data'][a]['title_short'] in music[0]:
                     URL = url['data'][a]['link']
                     break
             except IndexError:
                try:
                   try: 
                      url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
                   except:
                      url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
                   try:
                      if url['error']['message'] == "Quota limit exceeded":
                       raise QuotaExceeded("Too much requests limit yourself")
                   except KeyError:
                      None
                   for a in range(url['total'] + 1):
                       if music[0].split(" ")[0] in url['data'][a]['title']:
                        URL = url['data'][a]['link']
                        break
                except IndexError:
                   raise TrackNotFound("Track not found: " + song)
             self.download(URL, dir)
          try:   
             os.rename(dir + URL.split("/")[-1] + ".mp3" , dir + name)
          except FileNotFoundError:
             None
          try:   
             image = requests.get(image).content
          except:
             image = requests.get(image).content
          try:
             tag = EasyID3(dir + name)
             tag.delete()
          except mutagen.id3.ID3NoHeaderError:
             tag = mutagen.File(dir + name, easy=True)
             tag.add_tags()
          except:
             return dir + name
          tag['artist'] = artist[0]
          tag['title'] = music[0]
          tag['date'] = year[0]
          tag['album'] = album[0]
          tag['tracknumber'] = str(tracknum[0])
          tag['discnumber'] = str(discnum[0])
          tag['genre'] = " & ".join(genre)
          tag['albumartist'] = ", ".join(ar_album)
          tag.save(v2_version=3)
          audio = ID3(dir + name)
          audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
          audio.save()
          return dir + name
      def download_albumdee(self, URL, output=localdir + "/Songs/", check=True):
          if output == localdir + "/Songs":
           if not os.path.isdir("Songs"):
            os.makedirs("Songs")
          array = []
          music = []
          artist = []
          album = []
          tracknum = []
          discnum = []
          year = []
          genre = []
          ar_album = []
          urls = []
          names = []
          if "?" in URL:
           URL,a = URL.split("?")
          URL = "http://www.deezer.com/album/" + URL.split("/")[-1]
          try: 
             url = json.loads(requests.get("http://api.deezer.com/album/" + URL.split("/")[-1], headers=header).text)
          except:
             url = json.loads(requests.get("http://api.deezer.com/album/" + URL.split("/")[-1], headers=header).text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             if url['error']['message'] == "no data" or url['error']['message'] == "Invalid query":
              raise InvalidLink("Invalid link ;)")
          except KeyError:
             None
          try:
             image = url['cover_xl'].replace("1000", "1200")
          except:
             try:
                image = requests.get(URL).text
             except:
                image = requests.get(URL).text
             image = BeautifulSoup(image, "html.parser").find("img", class_="img_main").get("src").replace("200", "1200")
          for a in url['tracks']['data']:
              music.append(a['title'])
              urls.append(a['link'])
          for a in url['tracks']['data']:
              del array[:]
              try:
                 ur = json.loads(requests.get("https://api.deezer.com/track/" + str(a['id'])).text)
              except:
                 ur = json.loads(requests.get("https://api.deezer.com/track/" + str(a['id'])).text)
              try:
                 if ur['error']['message'] == "Quota limit exceeded":
                  raise QuotaExceeded("Too much requests limit yourself")
              except KeyError:
                 None
              tracknum.append(ur['track_position'])
              discnum.append(ur['disk_number'])
              for a in ur['contributors']:
                  array.append(a['name'])
              if len(array) > 1:
               for a in array:
                   for b in range(len(array)):
                       try:
                          if a in array[b] and a != array[b]:
                           del array[b]
                       except IndexError:
                          break
              artist.append(", ".join(array))
          album.append(url['title'])
          year.append(url['release_date'])
          try:
             for a in url['genres']['data']:
                 genre.append(a['name'])
          except KeyError:
             None
          for a in url['contributors']:
              if a['role'] == "Main":
               ar_album.append(a['name'])
          dir = str(output) + "/" + album[0].replace("/", "") + "/"
          try:
             if not os.path.isdir(dir):
              os.makedirs(dir)
          except:
             None
          try:   
             image = requests.get(image).content
          except:
             image = requests.get(image).content
          for a in tqdm(range(len(urls))):
              name = artist[a].replace("/", "") + " " + music[a].replace("/", "") + ".mp3"
              names.append(dir + name)
              if os.path.isfile(dir + name):
               if check == False:
                continue
               print(dir + name)
               ans = input("Song already exist do you want to redownload it?(y or n):")
               if not ans == "y":
                return
              try:
                 self.download(urls[a], dir)
              except TrackNotFound:
                 try:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "") + " + " + artist[a].replace("#", "")).text)
                 except:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "") + " + " + artist[a].replace("#", "")).text)
                 try:
                    if url['error']['message'] == "Quota limit exceeded":
                     raise QuotaExceeded("Too much requests limit yourself")
                 except KeyError:
                    None
                 try:
                    for b in range(url['total'] + 1):
                        if url['data'][b]['title'] == music[a] or url['data'][b]['title_short'] in music[a]:
                         URL = url['data'][b]['link']
                         break
                 except IndexError:
                    try:
                       try: 
                          url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "").split(" ")[0] + " + " + artist[a].replace("#", "")).text)
                       except:
                          url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "").split(" ")[0] + " + " + artist[a].replace("#", "")).text)
                       try:
                          if url['error']['message'] == "Quota limit exceeded":
                           raise QuotaExceeded("Too much requests limit yourself")
                       except KeyError:
                          None
                       for b in range(url['total'] + 1):
                           if music[a].split(" ")[0] in url['data'][b]['title']:
                            URL = url['data'][b]['link']
                            break
                    except IndexError:
                       print("\nTrack not found: " + music[a] + " - " + artist[a])
                       continue
                 self.download(URL, dir)
                 urls[a] = URL
              try:
                 os.rename(dir + urls[a].split("/")[-1] + ".mp3", dir + name)
              except FileNotFoundError:
                 None
              try:
                 tag = EasyID3(dir + name)
                 tag.delete()
              except mutagen.id3.ID3NoHeaderError:
                 tag = mutagen.File(dir + name, easy=True)
                 tag.add_tags()
              except:
                 continue
              tag['artist'] = artist[a]
              tag['title'] = music[a]
              tag['date'] = year[0]
              tag['album'] = album[0]
              tag['tracknumber'] = str(tracknum[a])
              tag['discnumber'] = str(discnum[a])
              tag['genre'] = " & ".join(genre)
              tag['albumartist'] = ", ".join(ar_album)
              tag.save(v2_version=3)
              audio = ID3(dir + name)
              audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
              audio.save()
          return names
      def download_playlistdee(self, URL, output=localdir + "/Songs/", check=True):
          array = []
          if "?" in URL:
           URL,a = URL.split("?")
          try: 
             url = json.loads(requests.get("https://api.deezer.com/playlist/" + URL.split("/")[-1] + "/tracks").text)
          except:
             url = json.loads(requests.get("https://api.deezer.com/playlist/" + URL.split("/")[-1] + "/tracks").text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             if url['error']['message'] == "no data" or url['error']['message'] == "Invalid query":
              raise InvalidLink("Invalid link ;)")
          except KeyError:
             None
          for a in url['data']:
              array.append(self.download_trackdee(a['link'], output, check))
          return array
      def download_trackspo(self, URL, output=localdir + "/Songs/", check=True, playlist=False):
          global spo
          if output == localdir + "/Songs":
           if not os.path.isdir("Songs"):
            os.makedirs("Songs")
          array = []
          music = []
          artist = []
          album = []
          tracknum = []
          discnum = []
          year = []
          genre = []
          ar_album = []
          if not len(URL) == 53:
           URL,a = URL.split("?")
          if len(URL) != 53:
           raise InvalidLink("Invalid link ;)")
          try:
             url = spo.track(URL)
          except:
             token = generate_token()
             spo = spotipy.Spotify(auth=token)
             url = spo.track(URL)
          music.append(url['name'])
          for a in range(20):
              try:
                 array.append(url['artists'][a]['name'])
              except IndexError:
                 artist.append(", ".join(array))
                 del array[:]
                 break
          album.append(url['album']['name'])
          image = url['album']['images'][0]['url']
          tracknum.append(url['track_number'])
          discnum.append(url['disc_number'])
          year.append(url['album']['release_date'])
          for a in url['album']['artists']:
              ar_album.append(a['name'])
          try:    
             url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace("#", "")).text)
          except:
             url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "") + " + " + artist[0].replace("#", "")).text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          song = music[0] + " - " + artist[0]
          if playlist == False:
           try:
              for a in range(url['total'] + 1):
                  if (url['data'][a]['title'] == music[0] or url['data'][a]['title_short'] in music[0]) and url['data'][a]['album']['title'] == album[0]:
                   URL = url['data'][a]['link']
                   break
           except IndexError:
              try:
                 try:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
                 except:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
                 try:
                    if url['error']['message'] == "Quota limit exceeded":
                     raise QuotaExceeded("Too much requests limit yourself")
                 except KeyError:
                    None
                 for a in range(url['total'] + 1):
                     if music[0].split(" ")[0] in url['data'][a]['title']:
                      URL = url['data'][a]['link']
                      break
              except IndexError:
                 raise TrackNotFound("Track not found: " + song)
          elif playlist == True:
           try:
              for a in range(url['total'] + 1):
                  if (url['data'][a]['title'] == music[0] or url['data'][a]['title_short'] in music[0]) and url['data'][a]['album']['title'] == album[0]:
                   URL = url['data'][a]['link']
                   break
           except IndexError:
              try:
                 url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
              except:
                 url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[0].replace("#", "").split(" ")[0] + " + " + artist[0].replace("#", "")).text)
              try:
                 if url['error']['message'] == "Quota limit exceeded":
                  raise QuotaExceeded("Too much requests limit yourself")
              except KeyError:
                 None
              for a in range(url['total'] + 1):
                  if music[0].split(" ")[0] in url['data'][a]['title']:
                   URL = url['data'][a]['link']
                   break
          song = music[0] + " - " + artist[0]
          try:
             url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
          except:
             url = json.loads(requests.get("http://api.deezer.com/track/" + URL.split("/")[-1]).text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
          except:
             url1 = json.loads(requests.get("http://api.deezer.com/album/" + str(url['album']['id']), headers=header).text)
          try:
             if url1['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             for a in url1['genres']['data']:
                 genre.append(a['name'])
          except KeyError:
             None
          dir = str(output) + "/" + artist[0].replace("/", "") + "/"
          try:
             if not os.path.isdir(dir):
              os.makedirs(dir)
          except:
             None
          name = artist[0].replace("/", "") + " " + music[0].replace("/", "") + ".mp3"
          if os.path.isfile(dir + name):
           if check == False:
            return dir + name
           ans = input("Song already exist do you want to redownload it?(y or n):")
           if not ans == "y":
            return
          print("\nDownloading:" + song)
          self.download(URL, dir)
          try:
             os.rename(dir + URL.split("/")[-1] + ".mp3" , dir + name)
          except FileNotFoundError:
             None
          try:
             image = requests.get(image).content
          except:
             image = requests.get(image).content
          try:
             tag = EasyID3(dir + name)
             tag.delete()
          except mutagen.id3.ID3NoHeaderError:
             tag = mutagen.File(dir + name, easy=True)
             tag.add_tags()
          except:
             return dir + name
          tag['artist'] = artist[0]
          tag['title'] = music[0]
          tag['date'] = year[0]
          tag['album'] = album[0]
          tag['tracknumber'] = str(tracknum[0])
          tag['discnumber'] = str(discnum[0])
          tag['genre'] = " & ".join(genre)
          tag['albumartist'] = ", ".join(ar_album)
          tag.save(v2_version=3)
          audio = ID3(dir + name)
          audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
          audio.save()
          return dir + name
      def download_albumspo(self, URL, output=localdir + "/Songs/", check=True):
          global spo
          if output == localdir + "/Songs":
           if not os.path.isdir("Songs"):
            os.makedirs("Songs")
          array = []
          music = []
          artist = []
          album = []
          tracknum = []
          discnum = []
          year = []
          genre = []
          ar_album = []
          urls = []
          names = []
          if not len(URL) == 53:
           URL,a = URL.split("?")
          if len(URL) != 53: 
           raise InvalidLink("Invalid link ;)")
          try:
             tracks = spo.album(URL)
          except:
             token = generate_token()
             spo = spotipy.Spotify(auth=token)
             tracks = spo.album(URL)
          album.append(tracks['name'])
          for a in tracks['artists']:
              ar_album.append(a['name'])
          for track in tracks['tracks']['items']:
              music.append(track['name'])
              tracknum.append(track['track_number'])
              discnum.append(track['disc_number'])
          for artists in tracks['tracks']['items']:
              for a in range(20):
                  try:
                     array.append(artists['artists'][a]['name'])
                  except IndexError:
                     artist.append(", ".join(array))
                     del array[:]
                     break
          year.append(tracks['release_date'])
          image = tracks['images'][0]['url']
          for a in range(tracks['total_tracks'] // 50):
              try:
                 tracks = spo.next(tracks['tracks'])
              except:
                 token = generate_token()
                 spo = spotipy.Spotify(auth=token)
                 tracks = spo.next(tracks)['items']
              for track in tracks['items']:
                  music.append(track['name'])
                  tracknum.append(track['track_number'])
                  discnum.append(track['disc_number'])
              for artists in tracks['items']:
                  for a in range(20):
                      try:
                         array.append(artists['artists'][a]['name'])
                      except IndexError:
                         artist.append(", ".join(array))
                         del array[:]
                         break
          artis = tracks['artists'][0]['name']
          dir = str(output) + "/" + album[0].replace("/", "") + "/"
          try:
             if not os.path.isdir(dir):
              os.makedirs(dir)
          except:
             None
          try:   
             url = json.loads(requests.get('https://api.deezer.com/search/?q=artist:"' + artis.replace("#", "") + '" album:"' + album[0].replace("#", "") + '"').text)
          except:
             url = json.loads(requests.get('https://api.deezer.com/search/?q=artist:"' + artis.replace("#", "") + '" album:"' + album[0].replace("#", "") + '"').text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          try:
             for a in range(url['total'] + 1):
                 if url['data'][a]['album']['title'] == album[0]:
                  URL = str(url['data'][a]['album']['id'])
                  break
          except IndexError:
             raise AlbumNotFound("Album not found: " + album[0])
          try:   
             url = json.loads(requests.get("https://api.deezer.com/album/" + URL, headers=header).text)
          except:
             url = json.loads(requests.get("https://api.deezer.com/album/" + URL, headers=header).text)
          try:
             if url['error']['message'] == "Quota limit exceeded":
              raise QuotaExceeded("Too much requests limit yourself")
          except KeyError:
             None
          for a in url['tracks']['data']:
              urls.append(a['link'])
          try:
             for a in url['genres']['data']:
                 genre.append(a['name'])
          except KeyError:
             None
          try:   
             image = requests.get(image).content
          except:
             image = requests.get(image).content   
          if len(urls) < len(music):
           idk = len(urls)
          elif len(urls) > len(music):
           idk = len(music)
          else:
              idk = len(urls)
          for a in tqdm(range(idk)):
              name = artist[a].replace("/", "") + " " + music[a].replace("/", "") + ".mp3"
              names.append(dir + name)
              if os.path.isfile(dir + name):
               if check == False:
                continue
               print(dir + name)
               ans = input("Song already exist do you want to redownload it?(y or n):")
               if not ans == "y":
                return
              try:
                 self.download(urls[a], dir)
              except TrackNotFound:
                 try:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "") + " + " + artist[a].replace("#", "")).text)
                 except:
                    url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "") + " + " + artist[a].replace("#", "")).text)
                 try:
                   if url['error']['message'] == "Quota limit exceeded":
                    raise QuotaExceeded("Too much requests limit yourself")
                 except KeyError:
                    None
                 try:
                    for b in range(url['total'] + 1):
                        if url['data'][b]['title'] == music[a] or url['data'][b]['title_short'] in music[a]:
                         URL = url['data'][b]['link']
                         break
                 except IndexError:
                    try:
                       try: 
                          url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "").split(" ")[0] + " + " + artist[a].replace("#", "")).text)
                       except:
                          url = json.loads(requests.get("https://api.deezer.com/search/track/?q=" + music[a].replace("#", "").split(" ")[0] + " + " + artist[a].replace("#", "")).text)
                       try:
                          if url['error']['message'] == "Quota limit exceeded":
                           raise QuotaExceeded("Too much requests limit yourself")
                       except KeyError:
                          None
                       for b in range(url['total'] + 1):
                           if music[a].split(" ")[0] in url['data'][b]['title']:
                            URL = url['data'][b]['link']
                            break
                    except IndexError:
                       print("\nTrack not found: " + music[a] + " - " + artist[a])
                       continue
                 self.download(URL, dir)
                 urls[a] = URL
              try:
                 os.rename(dir + urls[a].split("/")[-1] + ".mp3", dir + name)
              except FileNotFoundError:
                 None
              try:
                 tag = EasyID3(dir + name)
                 tag.delete()
              except mutagen.id3.ID3NoHeaderError:
                 tag = mutagen.File(dir + name, easy=True)
                 tag.add_tags()
              except:
                 continue
              tag['artist'] = artist[a]
              tag['title'] = music[a]
              tag['date'] = year[0]
              tag['album'] = album[0]
              tag['tracknumber'] = str(tracknum[a])
              tag['discnumber'] = str(discnum[a])
              tag['genre'] = " & ".join(genre)
              tag['albumartist'] = ", ".join(ar_album)
              tag.save(v2_version=3)
              audio = ID3(dir + name)
              audio['APIC'] = APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=image)
              audio.save()
          return names
      def download_playlistspo(self, URL, output=localdir + "/Songs/", check=True):
          global spo
          array = []
          if not len(URL) == 87 and not len(URL) == 69:
           URL,a = URL.split("?")
          if len(URL) != 87 and len(URL) != 69:
           raise InvalidLink("Invalid link ;)")
          URL = URL.split("/")
          try:
             tracks = spo.user_playlist_tracks(URL[-3], playlist_id=URL[-1])
          except:
             token = generate_token()
             spo = spotipy.Spotify(auth=token)
             tracks = spo.user_playlist_tracks(URL[-3], playlist_id=URL[-1])
          for a in tracks['items']:
              try:
                 array.append(self.download_trackspo(a['track']['external_urls']['spotify'], output, check, True))
              except IndexError:
                 print("\nTrack not found " + a['track']['name'])
                 array.append(localdir + "/Songs/" + a['track']['name'])
          for a in range(tracks['total'] // 100):
              try:
                 tracks = spo.next(tracks)
              except:
                 token = generate_token()
                 spo = spotipy.Spotify(auth=token)
                 tracks = spo.next(tracks)
              for a in tracks['items']:
                  try:
                     array.append(self.download_trackspo(a['track']['external_urls']['spotify'], output, check, True))
                  except IndexError:
                     print("\nTrack not found " + a['track']['name'])
                     array.append(localdir + "/Songs/" + a['track']['name'])
          return array
      def download_name(self, artist, song, output=localdir + "/Songs/", check=True):
          global spo
          try:
             search = spo.search(q="track:" + song + " artist:" + artist)
          except:
             token = generate_token()
             spo = spotipy.Spotify(auth=token)
             search = spo.search(q="track:" + song + " artist:" + artist)
          try:
             return self.download_trackspo(search['tracks']['items'][0]['external_urls']['spotify'], output, check)
          except IndexError:
             raise TrackNotFound("Track not found: " + artist + " - " + song)