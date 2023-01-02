from spotify import Spotify
from youtube import Youtube
from main import notify, getCorrect
import sys, getopt, shutil
import os 

class Spotify_Download():
    def __init__(self,type):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__uri = download_uri()
        self.__album = download_album()
        self.__file = download_file()
        self.__query = download_Query()
        self.__playlist = download_playlist()
        self.type = type

    def __downloadMusicFromYoutube(self, name, uri, dur):
        #finding song on youtube
        self.__youtube.get(name, dur)


        #downloading video from youtube
        if self.__youtube.download(
            url=self.__youtube.getResult(),
            path=uri,
            filename=uri
        ):
            #converting video to mp3 file
            self.__youtube.convertVideoToMusic(
                uri=uri
            )
            return True
        else:
            return False

    def __getSongInfoFromSpotify(self, uri):
        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None

    def getNameFromYoutube(self, url):
            return self.__youtube.getNameFromYoutube(url)

    def getData(self, uri):
        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None

    def getYoutubeMusicInfo(self, url):
        return self.__youtube.getNameFromYoutube(url)

    def download(self):
        if self.type == "uri":
            self.__uri.downloadBySpotifyUri()
        elif self.type == "album":
            self.__album.downloadBySpotifyUriAlbumMode()
        elif self.type == "file":
            self.__file.downloadBySpotifyUriFromFile()
        elif self.type == "query":
            self.__query.downloadBySearchQuery()
        else:
            self.__playlist.downloadBySpotifyUriPlaylistMode()

class download_uri(Spotify_Download):

    def downloadBySpotifyUri(self, uri, path):
        #get info
        info = self.__getSongInfoFromSpotify(uri)

        if info:
            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            if self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms']):

                print(info['uri'])

                self.__editor.setTags(
                    data=info
                )

                cachepath = os.getcwd() + '/cache'
                fullpath = os.getcwd() + '/Downloads'

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

                name = f'{info["artist"][0]} - {info["name"]}'

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                    f"{fullpath}/{getCorrect(name)}.mp3"
                )

                print(path)

                if path:

                    os.rename(
                        f"{fullpath}/{getCorrect(name)}.mp3",
                        f"{path}/{getCorrect(name)}.mp3"
                    )

                #deleting cache
                try:shutil.rmtree(f"cache/{info['uri']}")
                except:pass

                notify.send(f'{info["artist"][0]} - {info["name"]}')
                return True
        return False


class download_Query(Spotify_Download):
    def downloadBySearchQuery(self, query, path=None):

        #get info
        info = self.__spotify.search(query=query)

        if not info:
            info = self.__last.get(query)

        if info:

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try:
                shutil.rmtree(f"cache/{info['uri']}")
            except:
                pass

            notify.send(f'{info["artist"][0]} - {info["name"]}')
            return True, info
        else:
            return False, None

class download_file(Spotify_Download):

    def downloadBySpotifyUriFromFile(self, filename):
        try:

            with open(filename, 'r') as f:
                data = f.readlines()

        except FileNotFoundError:

            print(f'No such file or directory: "{filename}"')
            exit(2)

        #normalize
        try:data.remove('\n')
        except:pass
        links = [ str(item).replace('\n','') for item in data ]

        for i,song in zip(range(len(links)),links):
            print(f'[{i+1}] - {song}')
            try:
                state = self.downloadBySpotifyUri(str(song).split(':')[-1])
                if not state:
                    notify.send(f'Failed to download',True)
            except:
                print('Something went wrong!')

class download_playlist(Spotify_Download):
    def downloadBySpotifyUriPlaylistMode(self, playlist_uri, path):

        user = Spotify.User()
        playlist = user.getPlaylistTracks(playlist_uri)

        for info, i in zip(playlist,range(len(playlist))):

            print(f'Downloading {i+1} of {len(playlist)}')
            
            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            notify.send(f'{info["artist"][0]} - {info["name"]}')


class download_album(Spotify_Download):
    def downloadBySpotifyUriAlbumMode(self, album_uri, path):

        user = Spotify()
        playlist = user.getAlbum(album_uri)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

            print(f'Downloading {i+1} of {len(playlist["tracks"])}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and downloading from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            notify.send(f'{info["artist"][0]} - {info["name"]}')

    
    def downloadFromYoutubeMusic(self, url, info, path):

        print(info)

        uri = info['uri']

        notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

        #downloading video from youtube
        if self.__youtube.download(
            url=url,
            path=uri,
            filename=uri
        ):

            #converting video to mp3 file
            self.__youtube.convertVideoToMusic(
                uri=uri
            )

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try:shutil.rmtree(f"cache/{info['uri']}")
            except:pass

            notify.send(f'{info["artist"][0]} - {info["name"]}')
            return True, info
        else:
            return False, None

    def search(self, query):
        return self.__spotify.search(query=query)