import logging
import os
import sys
import time
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

# Global variables for rate limiting
user_last_command_time = {}
COMMAND_RATE_LIMIT = 5  # Example: limit user commands to once per 60 seconds

last_api_call_time = 0
API_RATE_LIMIT = 5  # Example: limit API requests to once per 60 seconds

# Rate limiting decorator for user commands
def rate_limit_commands(func):
    async def wrapper(update: Update, context):
        user_id = update.effective_user.id
        current_time = time.time()

        # Check if the user has used this command before
        if user_id in user_last_command_time:
            last_command_time = user_last_command_time[user_id]
            time_since_last_command = current_time - last_command_time

            if time_since_last_command < COMMAND_RATE_LIMIT:
                await update.message.reply_text(f"Please wait {int(COMMAND_RATE_LIMIT - time_since_last_command)} seconds before using this command again.")
                return

        # Update the last command time and proceed with the function
        user_last_command_time[user_id] = current_time
        await func(update, context)
    
    return wrapper

# Rate limiting decorator for API calls
def rate_limit_api(func):
    async def wrapper(*args, **kwargs):
        global last_api_call_time
        current_time = time.time()

        # Check if the API call rate limit is exceeded
        if current_time - last_api_call_time < API_RATE_LIMIT:
            logger.warning("API rate limit exceeded. Try again later.")
            return None  # Skip the API request if the rate limit is exceeded

        # Update the last API call time and proceed with the function
        last_api_call_time = current_time
        return await func(*args, **kwargs)
    
    return wrapper

# Your original functions, now with rate limiting applied

@rate_limit_commands
async def start(update: Update, context):
    """Handle the /start command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the bot!")

@rate_limit_commands
async def group_image_reply_search(update: Update, context):
    """Handle the group image reply search command."""
    # Logic for group image reply search
    pass

@rate_limit_api
async def image_search_link(update: Update, context):
    """Handle reverse image search."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait for your results...")
    # Your existing reverse image search logic here
    pass

@rate_limit_api
async def gif_image_search(update: Update, context):
    """Handle gif image search."""
    # Your gif image search logic here
    pass

@rate_limit_api
async def sticker_image_search(update: Update, context):
    """Handle sticker image search."""
    # Your sticker image search logic here
    pass

async def unknown(update: Update, context):
    """Handle unknown commands."""
    await update.message.reply_text("Sorry, I didn't understand that command.")

def has_photo(update: Update) -> bool:
    return update.message.photo is not None

def has_video_or_document(update: Update) -> bool:
    return update.message.video is not None or update.message.document is not None

def error(application: Application, context, error: TelegramError):
    """Log all errors from the telegram bot API."""
    logger.warning('Update "%s" caused error "%s"' % (context.update, error))

def main():
    application = Application.builder().token(settings.TELEGRAM_API_TOKEN).build()

    def stop_and_restart():
        """Gracefully stop the Application and replace the current process with a new one."""
        application.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update: Update, context):
        """Start the restarting process."""
        update.message.reply_text('Bot is restarting...')
        logger.info('Gracefully restarting...')
        Thread(target=stop_and_restart).start()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler('restart', restart, filters=filters.User(username='@<>')))
    application.add_handler(CommandHandler('reply_search', group_image_reply_search))
    application.add_handler(CommandHandler('best_match', best_match))
    application.add_handler(CallbackQueryHandler(callback_best_match))

    # Message handlers
    application.add_handler(MessageHandler(filters.PHOTO, image_search_link))
    application.add_handler(MessageHandler(filters.VIDEO, gif_image_search))
    application.add_handler(MessageHandler(filters.Document, gif_image_search))
    application.add_handler(MessageHandler(filters.Sticker, sticker_image_search))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Log all errors
    application.add_error_handler(error)

    application.run_polling()
    logger.info('Started bot. Waiting for requests...')
    application.idle()

if __name__ == '__main__':
    main()
