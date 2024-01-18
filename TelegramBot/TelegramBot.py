from enum import Enum, auto
import os
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .ChatFlow import ChatFlow

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
        self.conv_handler = ChatFlow.conversation_handler

    def send_message(self, id: str, text: str):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={id}&text={text}"
        print(requests.get(url).json()) # this sends the message

    def start_bot(self):
        self.create_conversation_handler()
        self.application.add_handler(self.conv_handler)
        self.application.add_error_handler(ChatFlow.chat_functions.error_handler)
        # Run the bot until the user presses Ctrl-C
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    # env = read_env('.env')
    bot = TelegramBot()
    bot.start_bot()
    # bot.send_message()
    