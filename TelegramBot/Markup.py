from telegram import ReplyKeyboardMarkup


class Keyboards:
    start_keyboard = [
        ["Get Current Cards"],
        ["Update Cards"],
        ["Done"]
    ]

    update_card_keybaord = [
        ["Add Card"],
        ["Delete Card"],
        ["Done"]
    ]


class Markup:
    start_markup = ReplyKeyboardMarkup(Keyboards.start_keyboard, one_time_keyboard=True)
    update_cards_markup = ReplyKeyboardMarkup(Keyboards.update_card_keybaord, one_time_keyboard=True)
