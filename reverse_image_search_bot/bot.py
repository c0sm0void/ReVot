import logging
import os
import sys
from threading import Thread

from telegram import Bot, Update, ForceReply
from telegram.error import TelegramError
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, filters, MessageHandler
from telegram.constants import MessageType

from queue import Queue
from . import settings
from .commands import best_match, callback_best_match, gif_image_search, group_image_reply_search, image_search_link, \
    start, sticker_image_search, unknown

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def has_photo(update: Update) -> bool:
    return update.message.photo is not None


def has_video_or_document(update: Update) -> bool:
    return update.message.video is not None or update.message.document is not None


def error(application: Application, context, error: TelegramError):
    """Log all errors from the telegram bot api

    Args:
        application (:obj:`telegram.Application`): Telegram Api Application Object.
        context (:obj:`telegram.ext.CallbackContext`): Telegram Api CallbackContext Object
        error (:obj:`telegram.error.TelegramError`): Telegram Api TelegramError Object
    """
    logger.warning('Update "%s" caused error "%s"' % (context.update, error))


def main():
    application = Application.builder().token(settings.TELEGRAM_API_TOKEN).build()

    def stop_and_restart():
        """Gracefully stop the Application and replace the current process with a new one."""
        application.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update: Update, context):
        """Start the restarting process

        Args:
            update (:obj:`telegram.update.Update`): Telegram Api Update Object
            context (:obj:`telegram.ext.CallbackContext`): Telegram Api CallbackContext Object
        """
        update.message.reply_text('Bot is restarting...')
        logger.info('Gracefully restarting...')
        Thread(target=stop_and_restart).start()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler('restart', restart, filters=filters.User(username='@<>')))
    application.add_handler(CommandHandler('reply_search', group_image_reply_search))
    application.add_handler(CommandHandler('best_match', best_match))
    application.add_handler(CallbackQueryHandler(callback_best_match))

    application.add_handler(MessageHandler(filters.PHOTO, image_search_link))
    application.add_handler(MessageHandler(filters.VIDEO, gif_image_search))
    application.add_handler(MessageHandler(filters.Document, gif_image_search))
    application.add_handler(MessageHandler(filters.Sticker, sticker_image_search))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # log all errors
    application.add_error_handler(error)

    application.run_polling()
    logger.info('Started bot. Waiting for requests...')
    application.idle()


if __name__ == '__main__':
    main()
