from dotenv import load_dotenv, find_dotenv

load_dotenv('/.env')

from time import sleep
from TelegramBot.TelegramBot import TelegramBot
from TelegramBot.MySql.MySql import MySql
from TelegramBot.MoxScraper.MoxScraper import MoxScraper
import pandas as pd

def read_env(path):
    with open(path) as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        key, value = line.strip().split('=')
        env[key] = value
    return env

def main():
    bot = TelegramBot()
    my_sql = MySql()
    mox_scraper = MoxScraper()

    cards = my_sql.list_all()['card_name'].unique().tolist()

    for item in cards:
        df = mox_scraper.format_for_retailer(mox_scraper.scrape_mox_df(item))

        if not df.empty:
            ids = my_sql.get_users_for_card(item)
            for id in ids:
                message = f'The following cards you are looking for are available:\n\n{df}'
                bot.send_message(id=id, text=message)

        sleep(5)

if __name__ =="__main__":
    main()
