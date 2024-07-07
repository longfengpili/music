# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 09:56:23
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 12:38:12


import re
from pathlib import Path

import mutagen
# from mutagen import File
from mutagen.id3 import TIT2, TPE1, TALB, COMM, APIC


class Song:

    def __init__(self, title: str, artist: str, file: str, album: str = None, comment: str = None, **kwargs: dict[[str, ], ]):
        self.title = title
        self.artist = artist
        self.file = Path(file)
        self.album = album
        self.comment = comment
        self.kwargs = kwargs

    @property
    def audio(self):
        return mutagen.File(self.file)

    def __repr__(self):
        return f"{self.title}({self.artist}) - {self.album}"

    def __getattr__(self, item: str):
        if item in self.kwargs:
            return self.kwargs.get(item)
        if item in self.audio.tags:
            return self.audio.tags.get(item)
        raise AttributeError(f"'Song' object has no attribute '{item}'")

    def __getattribute__(self, item: str):
        return super(Song, self).__getattribute__(item)

    @classmethod
    def from_file(cls, file: str):
        audio = mutagen.File(file)
        title = str(audio.tags.get('TIT2'))
        artist = str(audio.tags.get('TPE1'))
        file = Path(file)
        album = str(audio.tags.get('TALB'))
        comment = str(audio.tags.get('COMM::eng'))
        return cls(title, artist, file, album, comment)

    def save(self):
        audio = self.audio
        audio.tags.update({
            'TIT2': TIT2(encoding=3, text=self.title),
            'TPE1': TPE1(encoding=3, text=self.artist),
            'TALB': TALB(encoding=3, text=self.album),
            'COMM': COMM(encoding=3, lang='eng', text=self.comment),
            **self.kwargs
        })
        audio.save()
        return self

    def update(self, pattern: str, sep: str = '-'):
        filename = self.file.stem
        psplits = pattern.split(sep)
        psplits = [p.strip() for p in psplits]
        pattern = sep.join([f'(?P<{p}>.*?)' for p in psplits[:-1]]) + sep + f'(?P<{psplits[-1]}>.*?$)'
        res = re.match(pattern, filename)
        if res:
            for pattern in psplits:
                value = res.group(pattern).strip()
                setattr(self, pattern, value)
                self.save()
            return self
