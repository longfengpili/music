# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 12:44:16
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 14:32:00

import re
import sys
from pathlib import Path

from music.models import Song

import logging
mlogger = logging.getLogger(__name__)


def parse_shellparams(shellinputs):
    params = shellinputs[1:]
    args = [param for param in params if not re.match('--[a-zA-Z]+', param) and not param.count('=') > 0]
    dirpath = args[0] if args else None
    kwargs = dict(param[2:].split('=') for param in params if re.match('--[a-zA-Z]+', param) and param.count('=') == 1)
    others = [param for param in params if param not in args and param[2:].split('=')[0] not in kwargs]
    if others:
        raise SyntaxError(f'please check your shellparams 【{others}】, example: 【python mytest.py test --name=john】')
    return dirpath, kwargs


def get_songs(dirpath: str):
    dpath = Path(dirpath)
    songs = [file for file in dpath.rglob('*.mp3')]
    return songs


if __name__ == '__main__':
    shellinputs = sys.argv
    dirpath, kwargs = parse_shellparams(shellinputs)

    if not dirpath:
        raise ValueError('dirpath must be setting')

    songs = get_songs(dirpath)
    for song in songs:
        spath = song.as_posix()
        try:
            song = Song.from_file(spath)
            song = song.save()
            mlogger.info(song)
        except Exception as e:
            mlogger.error(f'{spath}[{e}]')
