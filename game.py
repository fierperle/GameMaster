import logging
import time
from pathlib import Path
from tkinter.ttk import Frame
from typing import List, Dict
from xml.etree import ElementTree

import main
from player import Player

logger = logging.getLogger("PyLog")


class GameInfo:
    def __init__(self, type, variant, status="En Cours", creation_date: str = time.asctime()[4:], end_date: str = "", filepath: str = ""):
        self.type = type
        self.variant = variant
        self.status = status
        self.creation_date = creation_date
        self.end_date = end_date
        self.filepath = Path(filepath)


class Game:
    def __init__(self, players: List[Player], gameinfo=GameInfo(None, None)):
        self.__players = players
        self.__game_type = gameinfo.type
        self.__game_variant = gameinfo.variant

        self.__status = gameinfo.status

        self.__creation_date = gameinfo.creation_date
        self.__end_date = gameinfo.end_date

        self.frame = None

    @classmethod
    def load(cls, game_creation_date):
        raise NotImplementedError()

    # TODO Generate Unique ID
    def save(self):
        main.GAMES[self.get_creation_date()] = self
        pass

    def pause(self):
        self.__status = "En pause"
        self.save()

    def end(self):
        self.__status = "Finie"
        self.__end_date = time.asctime()[4:]
        self.save()

    def get_game_type(self):
        if self.__game_type is None and self.__game_variant is None:
            return ""
        elif self.__game_variant is None:
            return self.__game_type
        else:
            return self.__game_type + "-" + self.__game_variant

    def get_creation_date(self):
        return self.__creation_date

    def get_players(self):
        return self.__players

    def get_players_with(self, prop: str, value: object):
        return [player for player in self.__players if player.get(prop) == value]

    def get_status(self):
        return self.__status

    @classmethod
    def start(cls):
        raise NotImplementedError()


def load_all() -> Dict[str, GameInfo]:
    games = {}
    path = Path("data/saves/games.xml")
    if not path.exists():
        logger.info("No game save")
        pass
    with path.open() as file:
        root = ElementTree.parse(file).getroot()
        if root.tag != "games":
            logger.warning("Corrupted file: %s", path.name)
            pass
        game_elements = root.findall("game")
        logger.info("Find %s game saves", len(game_elements))
        for game in game_elements:
            pass
    return games


def save_all(games):
    pass
