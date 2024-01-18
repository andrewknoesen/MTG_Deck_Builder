from telegram import ReplyKeyboardMarkup


class Keyboards:
    start_bot = [['/start']]

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
    def convert_to_linear_keyboard(l: list):
        return_list = []
        for i in l:
            return_list.append([i])
        return ReplyKeyboardMarkup(return_list, one_time_keyboard=True)

    start_markup = ReplyKeyboardMarkup(Keyboards.start_keyboard, one_time_keyboard=True)
    update_cards_markup = ReplyKeyboardMarkup(Keyboards.update_card_keybaord, one_time_keyboard=True)
    start_bot = ReplyKeyboardMarkup(Keyboards.start_bot, one_time_keyboard=True)
