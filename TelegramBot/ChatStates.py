from enum import Enum, auto


class States(Enum):
    CHOOSING = auto()
    UPDATE_CARDS = auto()
    DELETE_CARDS = auto()
    ADD_CARDS = auto()
    
    ASK_CONFIRM = auto()
    REVIEW = auto()