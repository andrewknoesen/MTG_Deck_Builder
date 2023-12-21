import asyncio
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .Markup import Markup

from .ChatStates import States
from .Scryfall.Scryfall import Scryfall
from .MySql.MySql import MySql


class ChatFunctions:
    def __init__(self) -> None:
        self.my_sql = MySql('root', 'my_root_password', 'card_database')
        self.scryfall = Scryfall()

    async def done(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Display the gathered info and end the conversation."""
        await update.message.reply_text(
            f"Cheers!",
            reply_markup=ReplyKeyboardRemove(),
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
        """Start the conversation and ask user for input."""
        cards = self.my_sql.get_user_cards(update.message.from_user.id)
        await update.message.reply_text(
            f"Your cards are: \n{cards}",
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
