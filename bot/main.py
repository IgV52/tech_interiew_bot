import logging.config
from bot import settings

from telegram.ext import Updater, MessageHandler, Filters

from bot.logging_config import LOGGING_CONFIG
from telegram.ext import Updater
from bot.conversation.conv_main import conv_talk, conv_reg
from bot.handlers import save_document


def main():

    mybot = Updater(settings.BOT_API, use_context=True)

    dp = mybot.dispatcher

    dp.add_handler(conv_talk)
    dp.add_handler(conv_reg)
    dp.add_handler(MessageHandler(Filters.document, save_document))

    logging.config.dictConfig(LOGGING_CONFIG)

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
