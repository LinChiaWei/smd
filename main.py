#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from download_song import *
import sys, getopt, shutil
import os, re, random
import notify2
from pygame import mixer


class MusicDownloader(object):
    def __init__(self,type):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__uri = download_uri()
        self.__album = download_album()
        self.__file = download_file()
        self.__query = download_Query()
        self.__playlist = download_playlist()
        self.type = type

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



class CLI(object):

    path = None

    @staticmethod
    def logo():

        print(u'''

_____/\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\\\____________/\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\____
 ___/\\\\\\/////////\\\\\\_\\/\\\\\\\\\\\\________/\\\\\\\\\\\\_\\/\\\\\\////////\\\\\\__
  __\\//\\\\\\______\\///__\\/\\\\\\//\\\\\\____/\\\\\\//\\\\\\_\\/\\\\\\______\\//\\\\\\_
   ___\\////\\\\\\_________\\/\\\\\\\\///\\\\\\/\\\\\\/_\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
    ______\\////\\\\\\______\\/\\\\\\__\\///\\\\\\/___\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
     _________\\////\\\\\\___\\/\\\\\\____\\///_____\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
      __/\\\\\\______\\//\\\\\\__\\/\\\\\\_____________\\/\\\\\\_\\/\\\\\\_______/\\\\\\__
       _\\///\\\\\\\\\\\\\\\\\\\\\\/___\/\\\\\\_____________\/\\\\\\_\/\\\\\\\\\\\\\\\\\\\\\\\\/___
        ___\\///////////_____\\///______________\\///__\\////////////_____

        ''')

    @staticmethod
    def help():

        CLI.logo()

        print('\t\t       Spotify Music Downloader')
        print('\t\t         version 1.7.1-stable\n')

        print(' ./main.py [argument][value] - startup with arguments\n')

        print(' Arguments:\n')

        print('        -h,  --help                  Print a help message and exit.')
        print('        -p,  --path                  Set another directory.\n')

        print('        -ss, --spotify-song          Spotify song link or URI.')
        print('        -sa, --spotify-album         Spotify album link or URI.')
        print('        -sp, --spotify-playlist      Spotify playlist URI.\n')

        print('        -ds, --deezer-song           Deezer song link.')
        print('        -da, --deezer-album          Deezer album link.')
        print('        -dp, --deezer-playlist       Deezer playlist link.\n')

        print('        -ym, --youtube-music         YouTube Music link.')
        print('        -yv, --youtube-video         YouTube Video link.\n')

        print('        -a,  --apple                 Apple Music link.')
        print('        -q,  --query                 Search query.\n')

        print(' Note that your link has to be with quotation marks - "your_url"!\n')


    @staticmethod
    def main(argv):

        array = sys.argv

        for i in range(len(array)):

            if array[i] in ('-p','--path'):
                    CLI.path = array[i+1]

                    print(CLI.path)

        #same old for loop
        for i in range(len(array)):

            if array[i] in ('-h','--help'):

                CLI.help()

            else:
                try:
                    md = MusicDownloader()
                    state = md.download(argv)
                    if not state:
                            notify.send(f'Failed to download',True)
                except KeyboardInterrupt:
                    sys.exit(0)
                sys.exit(0)      

        CLI.help()




class notify(object):

    image = os.getcwd() + '/Data/icon.png'
    sound_info = os.getcwd() + '/Data/i.mp3'
    sound_warn = os.getcwd() + '/Data/w.mp3'
    try:notify2.init("Spotify Music Downloader Notifier")
    except:pass

    @staticmethod
    def sound(error=False):
        mixer.init()
        mixer.music.load(notify.sound_warn if error else notify.sound_info)
        mixer.music.play()

    @staticmethod
    def send(message, error=False, downloaded=True):
        try:
            ns = notify2.Notification(f'{"Downloaded" if downloaded else "Start downloading"}', message=message, icon=notify.image)
            # Set the urgency level
            ns.set_urgency(notify2.URGENCY_NORMAL)
            # Set the timeout
            ns.set_timeout(5000)
            notify.sound(error)
            ns.show()
        except:pass


def getCorrect(name):
    return re.sub(r"[\"#/@;:<>{}`+=~|.!?$%^&*№&]", string=name, repl='')


if __name__ == '__main__':

    CLI.main(sys.argv[1:])
