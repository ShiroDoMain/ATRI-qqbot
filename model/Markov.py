import json
import os
from random import choice
from typing import Dict, Generator, Tuple, Union


class Markov:
    content = {}

    def __init__(self, filename: str = "markov.json") -> None:
        self._content = {}
        self._file = filename
        # 状态保存在文件中
        if not os.path.exists(filename):
            self._save()
        self._load()

    def _save(self) -> None:
        with open(self._file, "w") as f:
            json.dump(self._content, f)

    def _load(self) -> None:
        with open(self._file, "r") as f:
            self._content = json.load(f)

    @property
    def content(self) -> Dict:
        return self._content

    def train(self, text) -> None:
        # 添加句子
        if text is None or len(text) < 4:
            return
        text_iter = self._process(text[3:])
        start = text[0:3]
        if start not in self._content:
            self._content[start] = []
        self._content[start].append(text[3])
        for c, n in text_iter:
            if c not in self._content:
                self._content[c] = []
            self._content[c].append(n)
        self._save()

    def _process(self, text: str) -> Generator:
        if not text.endswith("。"):
            text = text.rstrip() + "。"
        for i in range(len(text) - 1):
            yield text[i], text[i + 1]

    def gen(self, text, limit=20, _eval=False) -> Union[str, Tuple[str, bool]]:
        start = text[-1] if len(text) < 3 else text[-3:]
        if start not in self._content:
            return text if not _eval else (text, False)
        topic = ""
        while limit:
            arr = self._content[start]
            # 随机生成
            suffix = choice(arr)
            topic += suffix
            start = suffix
            if suffix == "。":
                _t = text+topic[:-1]
                return _t if not _eval else (_t, True)
            limit -= 1
        _t = text+topic
        return _t if not _eval else (_t, False)