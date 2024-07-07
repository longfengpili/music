# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 12:44:16
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 12:54:07

from pathlib import Path

from music.models import Song

import logging
mlogger = logging.getLogger(__name__)


def get_songs(dirpath: str):
    dpath = Path(dirpath)
    songs = [file for file in dpath.rglob('*.mp3')]
    return songs


if __name__ == '__main__':
    dirpath = 'e:/music'
    songs = get_songs(dirpath)
    
    for song in songs:
        spath = song.as_posix()
        song = Song.from_file(spath)
        song = song.update('artist-title')
        mlogger.info(song)
