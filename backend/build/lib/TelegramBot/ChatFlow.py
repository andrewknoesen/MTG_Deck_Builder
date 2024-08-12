import html
import json
import os
import traceback
from anyio import sleep
import pandas as pd
from telegram.constants import ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from CustomLogger.CustomLogger import log_error, log_message
from MoxScraper.MoxScraper import MoxScraper
from TelegramBot.Markup import Markup
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


from TelegramBot.ChatStates import States
from Scryfall.Scryfall import Scryfall
from MySql.MySql import MySql


DEVELOPER_CHAT_ID = os.environ['DEV_CHAT_ID']

class ChatFunctions:
    def __init__(self) -> None:
        self.my_sql = MySql()
        self.scryfall = Scryfall()
        self.mox_scraper = MoxScraper()

    async def done(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        await update.message.reply_text(
            f"Cheers!",
            reply_markup=Markup.start_bot,
        )

        return ConversationHandler.END

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask user for input."""
        await update.message.reply_text(
            "Greetings! \n"
            f"What would you like to do?",
            reply_markup=Markup.start_markup,
        )

        return States.CHOOSING

    async def get_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get the current cards in the db."""
        cards = self.my_sql.get_user_cards(update.message.from_user.id)
        await update.message.reply_text(
            f"Your cards are: \n{cards}",
            reply_markup=Markup.start_markup,
        )

        return States.CHOOSING

    async def scrape_current_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Scrape for the current cards in the db."""
        cards = self.my_sql.list_all(update.message.from_user.id)['card_name'].unique().tolist()
        log_message(f'Cards \n {cards}')
        await update.message.reply_text(
            'The following cards you are looking for are available:'
        )

        appended_df = pd.DataFrame()

        for item in cards:
            df = self.mox_scraper.format_for_retailer(self.mox_scraper.scrape_mox_df(item))
            if not df.empty:
                # Append the current DataFrame to the existing one
                appended_df = pd.concat([appended_df, df], ignore_index=True)
                
            

            await sleep(5)
        
        log_message(f"{appended_df}")
        # Plot DataFrame
        ratio = 3/2
        scale = 5
        x = scale * ratio
        y = x / (2/3)
        plt.figure(figsize=(x, y))  # Adjust size as needed
        plt.table(cellText=appended_df.values, colLabels=appended_df.columns, loc='center')
        plt.axis('off')  # Hide axis
        # plt.savefig('output.png', bbox_inches='tight', pad_inches=0.1, dpi=600)  # Save plot as image
        with PdfPages('output.pdf') as pdf:
            pdf.savefig(bbox_inches='tight', pad_inches=0.1)        
        plt.close()

        # Send the image to Telegram
        # with open('output.png', 'rb') as img:
        #     await update.message.reply_photo(img)
        with open('output.pdf', 'rb') as doc:
            await update.message.reply_document(doc)
            
        await update.message.reply_text(
            f"Scrape complete",
            reply_markup=Markup.start_markup,
        )

        return States.CHOOSING

    async def update_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Update the cards in the db"""
        await update.message.reply_text(
            "What operation would you like to do?",
            reply_markup=Markup.update_cards_markup,
        )

        return States.UPDATE_CARDS

    async def request_add_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Request what cards to add in the db"""

        await update.message.reply_text(
            "What is the name of the card you would like to add?",
        )

        return States.SEARCH_SCRYFALL

    async def search_scryfall(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Search scryfall"""

        cards: list = self.scryfall.search(update.message.text)
        cards.append('Redo search')
        await update.message.reply_text(
            "Which card you would like to add?",
            reply_markup=Markup.convert_to_linear_keyboard(cards)
        )

        return States.ADD_CARDS

    async def add_card_db(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Add cards in the db"""
        if update.message.text == "Redo search":
            await update.message.reply_text(
                "What is the name of the card you would like to add?",
            )
            return States.SEARCH_SCRYFALL

        self.my_sql.add_card(update.message.from_user.id, update.message.text)

        cards = self.my_sql.get_user_cards(update.message.from_user.id)
        await update.message.reply_text(
            f"Successfully added '{update.message.text}'\n"
            f"Current cards are: \n{cards}",
            reply_markup=Markup.start_markup,
        )

        return States.CHOOSING

    async def request_remove_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Request what cards to add in the db"""
        l = self.my_sql.get_user_cards(update.message.from_user.id, list_output=True)
        l.append('Cancel Delete')
        await update.message.reply_text(
            "What card do you want to delete?",
            reply_markup=Markup.convert_to_linear_keyboard(l)
        )

        return States.DELETE_CARDS

    async def remove_cards(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Remove cards in the db"""
        if update.message.text == 'Cancel Delete':
            await update.message.reply_text(
                "What would you like to do?",
                reply_markup=Markup.start_markup,
            )
            return States.CHOOSING
        
        self.my_sql.remove_card(
            update.message.from_user.id, update.message.text)

        cards = self.my_sql.get_user_cards(update.message.from_user.id)
        await update.message.reply_text(
            f"Successfully reomved '{update.message.text}'\n"
            f"\nCurrent cards are: \n{cards}",
            reply_markup=Markup.start_markup
        )

        return States.CHOOSING

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        log_error(f"Exception while handling an update: {context.error}")

        # traceback.format_exception returns the usual python message about an exception, but as a
        # list of strings rather than a single string, so we have to join them together.
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)

        # Build the message with some markup and additional information about what happened.
        # You might need to add some logic to deal with messages longer than the 4096 character limit.
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            "An exception was raised while handling an update\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
            f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # Finally, send the message
        await context.bot.send_message(
            chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        )


class ChatFlow:
    def __init__(self) -> None:
        pass
    chat_functions: ChatFunctions = ChatFunctions()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", chat_functions.start)],
        states={
            States.CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^Get Current Cards$"), chat_functions.get_cards
                ),
                MessageHandler(
                    filters.Regex(
                        "^Scrape Current Cards$"), chat_functions.scrape_current_cards
                ),
                MessageHandler(
                    filters.Regex(
                        "^Update Cards$"), chat_functions.update_cards
                ),
            ],
            States.UPDATE_CARDS: [
                MessageHandler(
                    filters.Regex(
                        "^Add Card$"), chat_functions.request_add_cards
                ),
                MessageHandler(
                    filters.Regex(
                        "^Delete Card$"), chat_functions.request_remove_cards
                ),
            ],
            States.ADD_CARDS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Done$")), chat_functions.add_card_db
                ),
            ],
            States.SEARCH_SCRYFALL: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Done$")), chat_functions.search_scryfall
                ),
            ],
            States.DELETE_CARDS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex(
                        "^Done$")), chat_functions.remove_cards
                ),
            ],

        },
        fallbacks=[MessageHandler(filters.Regex(
            "^Done$"), chat_functions.done)],
    )
