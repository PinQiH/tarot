import json
import os
import random
from typing import Tuple, Dict, Any

class TarotDeck:
    def __init__(self):
        self.tarot_data: Dict[str, Any] = {}
        with open("asset/Tarot.json", "rt", encoding="UTF-8") as fp:
            self.tarot_data = json.load(fp)
        self.tarot_path = "asset/TarotImages"
        self.deck: list[int] = []
        self.InitDeck()

    def InitDeck(self):
        self.deck = list(range(78)) # 共有78張牌
        random.shuffle(self.deck)

    def Pick(self) -> Tuple[str, str, str]:
        if not self.deck:
            self.InitDeck()

        idx = self.deck.pop() # 返回最後一張牌的索引
        path_suffix, data_key, name_prefix = IsReverse()

        fn = f"{idx:02d}{path_suffix}.jpg"
        tarot_path = os.path.join(self.tarot_path, fn)

        data = self.tarot_data[f"{idx:02d}"]
        tarot_name = data["name"]
        tarot_name = f"{name_prefix}{tarot_name}"
        tarot_info = data[data_key]

        return tarot_path, tarot_info, tarot_name


def IsReverse() -> Tuple[str, str, str]:
    # path_suffix, json_key, name_prefix
    pos = ("", "positive", "正位")
    rev = ("r", "reversed", "逆位")
    return pos if random.random() < 0.5 else rev
