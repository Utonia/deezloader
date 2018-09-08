# deezloader
This project has been created to download songs, albums or playlists with Spotify or Deezer link from Deezer.
* ### OS Supported ###
    ![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
    ![macOS Support](https://img.shields.io/badge/macOS-Support-brightgreen.svg)
    ![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)
* ### Installation ###
      pip3 install deezloader
### Download song
Download track by Spotify link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_trackspo("Insert the Spotify link of the track to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download track by Deezer link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_trackdee("Insert the Deezer link of the track to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download album
Download album by Spotify link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_albumspo("Insert the Spotify link of the album to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download album from Deezer link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_albumdee("Insert the Deezer link of the album to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download playlist
Download playlist by Spotify link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_playlistspo("Insert the Spotify link of the playlist to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
Download playlist from Deezer link
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_playlistdee("Insert the Deezer link of the playlist to download", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
### Download name
Download by name
```python
import deezloader
downloa = deezloader.Login("YOUR DEEZER EMAIL", "YOUR DEEZER PASSWORD")
downloa.download_name(artist="Eminem", song="Berzerk", output="SELECT THE PATH WHERE SAVE YOUR SONGS", check=True) #Or check=False for not check if song already exist
```
# Disclaimer
- I am not responsible for the usage of this program by other people.
- I do not recommend you doing this illegally or against Deezer's terms of service.
- This project is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)