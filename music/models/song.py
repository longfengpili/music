# -*- coding: utf-8 -*-
# @Author: chunyang.xu
# @Date:   2024-07-07 09:56:23
# @Last Modified by:   chunyang.xu
# @Last Modified time: 2024-07-07 14:11:00


import re
from pathlib import Path

import mutagen
from mutagen import File as afile
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

    @staticmethod
    def get_audio_tag(audio: afile, tag: str):
        frame = audio.tags.get(tag)
        if not frame:
            return None

        tvalue = frame.text[0]
        # 检查原始文本是否包含中文
        if re.search(r'[\u4e00-\u9fff1-9]+', tvalue):
            return tvalue

        # 尝试不同的编码解码方式
        encodings = ['latin1', 'utf-8', 'utf-16', 'utf-16-be']
        for encoding in encodings:
            try:
                tvalue_decoded = tvalue.encode(encoding).decode('gbk')
                if re.search(r'[\u4e00-\u9fff]+', tvalue_decoded):
                    return tvalue_decoded
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue

        return tvalue

    @classmethod
    def from_file(cls, file: str):
        audio = mutagen.File(file)
        title = cls.get_audio_tag(audio, 'TIT2')
        artist = cls.get_audio_tag(audio, 'TPE1')
        file = Path(file)
        album = cls.get_audio_tag(audio, 'TALB')
        comment = cls.get_audio_tag(audio, 'COMM::eng')
        return cls(title, artist, file, album, comment)

    def save(self):
        audio = self.audio
        audio.tags.add(TIT2(encoding=3, text=self.title))
        audio.tags.add(TPE1(encoding=3, text=self.artist))
        audio.tags.add(TALB(encoding=3, text=self.album))
        audio.tags.add(COMM(encoding=3, text=self.comment, lang='eng'))
        audio.save()
        return self

    def update_by_filename(self, pattern: str, sep: str = '-'):
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
