import time

from decouple import config

from .telegram_bot.bot import Bot
from .src.settings import TOKEN, PORT, SITE_URL


def run():
    bot = Bot(token=TOKEN, use_context=True)

    bot.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )
    bot.bot.setWebhook(SITE_URL + TOKEN)
    
    # bot.start_polling()

    bot.idle()