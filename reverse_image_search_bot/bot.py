import logging
import os
import sys
from threading import Thread

from telegram import Bot, TelegramError, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater

from . import settings
from .commands import (
    best_match,
    callback_best_match,
    gif_image_search,
    group_image_reply_search,
    image_search_link,
    start,
    sticker_image_search,
    unknown,
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update: Update, context):
    """Log all errors from the telegram bot API

    Args:
        update (:obj:`telegram.update.Update`): Telegram API Update Object
        context (:obj:`telegram.ext.CallbackContext`): Telegram API CallbackContext Object
    """
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(settings.TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher

    def stop_and_restart():
        """Gracefully stop the Updater and replace the current process with a new one."""
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update: Update, context):
        """Start the restarting process

        Args:
            update (:obj:`telegram.update.Update`): Telegram API Update Object
            context (:obj:`telegram.ext.CallbackContext`): Telegram API CallbackContext Object
        """
        update.message.reply_text('Bot is restarting...')
        logger.info('Gracefully restarting...')
        Thread(target=stop_and_restart).start()

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler('restart', restart, filters=Filters.user(username='@<>')))
    dispatcher.add_handler(CommandHandler('reply_search', group_image_reply_search))
    dispatcher.add_handler(CommandHandler('best_match', best_match, pass_args=True))
    dispatcher.add_handler(CallbackQueryHandler(callback_best_match))

    dispatcher.add_handler(MessageHandler(Filters.sticker, sticker_image_search))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_search_link))
    dispatcher.add_handler(MessageHandler(Filters.video | Filters.document, gif_image_search))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # log all errors
    dispatcher.add_error_handler(error)

    updater.start_polling()
    logger.info('Started bot. Waiting for requests...')
    updater.idle()


if __name__ == '__main__':
    main()