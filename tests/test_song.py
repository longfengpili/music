# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 10:06:39
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 12:25:38

from music.models.song import Song


class TestSongModel:

    def setup_method(self, method):
        self.file = 'e:/music/SHE - 恋人未满.mp3'

    def teardown_method(self, method):
        pass

    def test_song(self):
        song = Song.from_file(self.file)
        print(song.TIT2)
        print(song.title)
        
    def test_update(self):
        song = Song.from_file(self.file)
        s = song.update('artist-title')
        print(s)

