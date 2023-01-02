from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
from lastfm import LastFM
from apple import AppleMusic
from deezer import Deezer

class get_song_info():

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

    def getLastFMTags(self, name):
        return self.__last.get(name)

    def getYoutubeMusicInfo(self, url):
        return self.__youtube.getNameFromYoutube(url)
