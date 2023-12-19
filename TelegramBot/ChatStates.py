from enum import Enum, auto


class States(Enum):

    CHOOSING = auto()
    UPDATE_STOCKS = auto()
    DELETE_STOCK = auto()
    APPEND_STOCK = auto()
    EDIT_STOCK = auto()
    EDIT_STOCK_QUERY = auto()
    GET_NEWS = auto()

    ASK_CONFIRM = auto()
    REVIEW = auto()