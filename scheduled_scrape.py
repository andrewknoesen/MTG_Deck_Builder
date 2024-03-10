from dotenv import load_dotenv, find_dotenv
import matplotlib.pyplot as plt


load_dotenv('/.env')

from time import sleep
from TelegramBot.TelegramBot import TelegramBot
from MySql.MySql import MySql
from MoxScraper.MoxScraper import MoxScraper
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
    
    # Get users
    # Run list_all for user
    # run image gen
    
    users = my_sql.get_users()
    
    for user in users:
        cards = my_sql.list_all(user)['card_name'].unique().tolist()
        appended_df = pd.DataFrame()

        for item in cards:
            df = mox_scraper.format_for_retailer(mox_scraper.scrape_mox_df(item))
            if not df.empty:
                # Append the current DataFrame to the existing one
                appended_df = pd.concat([appended_df, df], ignore_index=True)

            sleep(5)
            
        # Plot DataFrame
        plt.figure(figsize=(8, 6))  # Adjust size as needed
        plt.table(cellText=appended_df.values, colLabels=appended_df.columns, loc='center')
        plt.axis('off')  # Hide axis
        plt.savefig('/output.png', bbox_inches='tight', pad_inches=0)  # Save plot as image
        plt.close()

        # Send the image to Telegram
        bot.send_image(id=user, image_path='/output.png')
            

    # cards = my_sql.list_all()['card_name'].unique().tolist()

    # for item in cards:
    #     df = mox_scraper.format_for_retailer(mox_scraper.scrape_mox_df(item))

    #     if not df.empty:
    #         ids = my_sql.get_users_for_card(item)
    #         for id in ids:
    #             message = f'The following cards you are looking for are available:\n\n{df}'
    #             bot.send_message(id=id, text=message)

    #     sleep(5)

if __name__ =="__main__":
    main()
