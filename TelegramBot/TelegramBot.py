from enum import Enum, auto
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from ChatStates import States

def read_env(path):
    with open(path) as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        key, value = line.strip().split('=')
        env[key] = value
    return env

class TelegramBot:
    def __init__(self, token = None):
        if not token:
            token = os.environ['TELEGRAM_TOKEN']
        
        self.token = token
        self.application = Application.builder().token(self.token).build()

    def create_conversation_handler(self):
        
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                States.CHOOSING: [
                    MessageHandler(
                        filters.Regex("^Get Current Stocks$"), self.get_stocks
                    ),
                    MessageHandler(filters.Regex(
                        "^Update Stock list$"), self.query_update_stocks),
                    MessageHandler(filters.Regex("^Get News$"), self.get_news_request),
                ],
                States.UPDATE_STOCKS: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.update_stocks
                    )
                ],
                States.DELETE_STOCK: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.delete_stock
                    )
                ],
                States.APPEND_STOCK: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.append_stock
                    )
                ],
                States.EDIT_STOCK_QUERY: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.edit_stock_query
                    )
                ],
                States.EDIT_STOCK: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.edit_stock
                    )
                ],
                States.GET_NEWS: [
                    MessageHandler(
                        filters.TEXT & ~(filters.COMMAND | filters.Regex(
                            "^Done$")), self.get_news
                    )
                ]
            },
            fallbacks=[MessageHandler(filters.Regex("^Done$"), self.done)],
        )

    def start_bot(self):
        self.application.add_handler(self.conv_handler)

        # Run the bot until the user presses Ctrl-C
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    env = read_env('.env')
    bot = TelegramBot(token=env['TELEGRAM_TOKEN'])
    bot.start_bot()
    