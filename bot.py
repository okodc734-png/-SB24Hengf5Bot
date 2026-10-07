import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🎵 Latest Music",
                callback_data="latest_music"
            )
        ],
        [
            InlineKeyboardButton(
                "🔥 Trending Songs",
                callback_data="trending"
            )
        ],
        [
            InlineKeyboardButton(
                "🎤 Artists",
                callback_data="artists"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Music Updates",
                callback_data="updates"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ About Us",
                callback_data="about"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_text = """
<b>🎵 Welcome to MusicHub!</b>

Discover music updates, new releases,
featured artists, and trending songs.

Choose an option below 👇
"""

    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if query.data == "latest_music":

        text = """
<b>🎵 Latest Music</b>

Discover the latest music releases,
new songs, and fresh music updates.

Stay tuned for new releases! 🎧
"""

    elif query.data == "trending":

        text = """
<b>🔥 Trending Songs</b>

Explore songs and artists currently
getting attention from music fans.

Discover what's trending today! 🎶
"""

    elif query.data == "artists":

        text = """
<b>🎤 Featured Artists</b>

Discover featured artists, new talent,
and music creators from around the world.

More artist updates coming soon! 🎤
"""

    elif query.data == "updates":

        text = """
<b>📢 Music Updates</b>

Get updates about new releases,
music news, featured songs, and artists.

Stay connected with MusicHub! 🎵
"""

    elif query.data == "about":

        text = """
<b>ℹ️ About MusicHub</b>

MusicHub is a music discovery bot
created to provide music updates,
new releases, trending songs, and
artist information.

Thank you for joining us! 🎶
"""

    else:
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="menu"
            )
        ]
    ]

    await query.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        """
<b>🏠 MusicHub Menu</b>

Choose an option below 👇
""",
        parse_mode="HTML",
        reply_markup=main_menu()
    )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while processing update:",
        exc_info=context.error
    )


def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing. "
            "Add BOT_TOKEN in Railway Variables."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            menu_handler,
            pattern="^menu$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_error_handler(error_handler)

    print("Music bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
