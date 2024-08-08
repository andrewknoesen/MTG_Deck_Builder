from enum import Enum, auto


class States(Enum):
    CHOOSING = auto()
    UPDATE_CARDS = auto()
    DELETE_CARDS = auto()
    ADD_CARDS = auto()
    SEARCH_SCRYFALL = auto()
    VALIDATE_CARD = auto()
    
    ASK_CONFIRM = auto()
    REVIEW = auto()