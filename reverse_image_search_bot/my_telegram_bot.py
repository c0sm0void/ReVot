from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
import logging

# Enable logging to help debug any issues
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for search history (use a dictionary with user_id as the key)
search_history = {}

# Replace with your bot's token from BotFather
TOKEN = "You API key"

# Start command: Welcomes the user and explains the bot's functionality
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(f"Hello {user.first_name}! Send me an image and I will search for it.")

# Function to handle the image search
def handle_image_search(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    # Simulating an image search (in real-world use, this is where the reverse image search code would go)
    search_result = "Search result for the uploaded image"

    # Storing the result in the user's search history
    if user_id not in search_history:
        search_history[user_id] = []
    
    search_history[user_id].append(search_result)
    
    # Inform the user about the search result
    update.message.reply_text(f"Here is the result for your image: {search_result}\n\nUse /history to view your past searches.")

# Command to show search history
def history(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    # Check if the user has any search history
    if user_id in search_history and search_history[user_id]:
        history_message = "Your past searches:\n"
        for idx, result in enumerate(search_history[user_id], 1):
            history_message += f"{idx}. {result}\n"
        update.message.reply_text(history_message)
    else:
        update.message.reply_text("You don't have any search history yet.")

# Error handler
def error(update, context):
    logger.warning(f'Update {update} caused error {context.error}')

# Main function to set up the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(MessageHandler(Filters.photo, handle_image_search))

    # Log all errors
    dp.add_error_handler(error)

    # Start polling for updates
    updater.start_polling()

    # Keep the bot running until interrupted
    updater.idle()

if __name__ == '__main__':
    main()
