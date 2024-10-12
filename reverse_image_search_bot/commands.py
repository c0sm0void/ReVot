import io
import os
from tempfile import NamedTemporaryFile
from uuid import uuid4

from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CallbackContext

from reverse_image_search_bot.utils import dict_to_str
from .image_search import BingReverseImageSearchEngine, GoogleReverseImageSearchEngine, IQDBReverseImageSearchEngine, TinEyeReverseImageSearchEngine, YandexReverseImageSearchEngine

from ratelimit import limits, sleep_and_retry

# Allow up to 5 requests per minute (adjust as needed)
MAX_CALLS = 5
PERIOD = 60  # In seconds (1 minute)

@sleep_and_retry
@limits(calls=MAX_CALLS, period=PERIOD)
async def limited_image_search(update: Update, context: CallbackContext):
    """Handles image search requests with rate limiting."""
    try:
        # Notify the user that their request is being processed
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Please wait for your results ...')

        # Check if the update contains a photo or document
        if update.effective_message.photo:
            photo = update.effective_message.photo[-1]  # Get the highest resolution version of the photo
        elif update.effective_message.document:
            if not update.effective_message.document.mime_type.startswith('image/'):
                await context.bot.send_message(chat_id=update.effective_chat.id, text='Unsupported file format. Please send an image.')
                return
            photo = update.effective_message.document
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No image found.')
            return

        # Retrieve the file and prepare it for image search
        file = await photo.get_file()
        image_buffer = io.BytesIO()
        image_buffer.write(await file.download_as_bytearray())
        image_buffer.seek(0)

        # Perform the reverse image search
        async with io.BufferedReader(image_buffer) as image_file:
            await general_image_search(context.bot, update, image_file)

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'An error occurred: {str(e)}')

async def start(update: Update, context: CallbackContext):
    """Send Start / Help message to client."""
    try:
        reply = """*ReVot - Reverse Image Search Bot (MS AZURE OR LOCAL)*

(Currently for testing not active all time, you know it's costly ;p)

*How to use me*
Send me images or stickers and I will send you direct reverse image search links for IQDB, Google, TinEy, Yandex and Bing.

*Commands*
- /help, /start: show a help message with information about the bot and its usage.

Thank you for using.
(cosmos)
"""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.MARKDOWN)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_dir = os.path.join(current_dir, 'images/example_usage.png')

        if os.path.exists(image_dir):
            async with aiofiles.open(image_dir, 'rb') as f:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f, caption='Example Usage')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Example image not found.')
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'An error occurred: {str(e)}')


async def gif_image_search(update: Update, context: CallbackContext):
    """Send a reverse image search link for the GIF sent to us."""
    try:
        await update.message.reply_text('Please wait for your results ...')
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

        document = update.message.document or update.message.video
        video = await context.bot.get_file(document.file_id)

        with NamedTemporaryFile() as video_file:
            await video.download(out=video_file)
            video_clip = VideoFileClip(video_file.name, audio=False)

            with NamedTemporaryFile(suffix='.gif') as gif_file:
                video_clip.write_gif(gif_file.name)

                dirname = os.path.dirname(gif_file.name)
                file_name = os.path.splitext(gif_file.name)[0]
                compressed_gif_path = os.path.join(dirname, file_name + '-min.gif')

                await compress_gif(compressed_gif_path, gif_file.name)

                if os.path.isfile(compressed_gif_path):
                    await general_image_search(context.bot, update, compressed_gif_path, 'gif')
                else:
                    await general_image_search(context.bot, update, gif_file.name, 'gif')

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'An error occurred: {str(e)}')


async def compress_gif(output_path, input_path):
    """Asynchronously compress GIF."""
    pass  # Implement your async GIF compression logic


async def sticker_image_search(update: Update, context: CallbackContext):
    """Send a reverse image search link for the image of the sticker sent to us."""
    try:
        await update.message.reply_text('Please wait for your results ...')
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

        sticker_image = await context.bot.get_file(update.message.sticker.file_id)
        converted_image = io.BytesIO()

        async with io.BytesIO() as image_buffer:
            await sticker_image.download(out=image_buffer)
            async with io.BufferedReader(image_buffer) as image_file:
                pil_image = Image.open(image_file).convert("RGBA")
                pil_image.save(converted_image, 'png')

                await general_image_search(context.bot, update, converted_image, 'png')
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'An error occurred: {str(e)}')


async def image_search_link(update: Update, context: CallbackContext):
    """Send a reverse image search link for the image sent by the client."""
    await limited_image_search(update, context)


class ReverseImageSearchHandler:
    """Handles reverse image search for multiple engines."""
    def __init__(self):
        self.iqdb_search = IQDBReverseImageSearchEngine()
        self.google_search = GoogleReverseImageSearchEngine()
        self.tineye_search = TinEyeReverseImageSearchEngine()
        self.bing_search = BingReverseImageSearchEngine()
        self.yandex_search = YandexReverseImageSearchEngine()

    async def search_image(self, image_file, image_extension: str = 'jpg'):
        image_url = self.iqdb_search.upload_image(image_file, 'irs-' + str(uuid4())[:8] + '.' + image_extension)
        return {
            'iqdb_url': self.iqdb_search.get_search_link_by_url(image_url),
            'google_url': self.google_search.get_search_link_by_url(image_url),
            'tineye_url': self.tineye_search.get_search_link_by_url(image_url),
            'bing_url': self.bing_search.get_search_link_by_url(image_url),
            'yandex_url': self.yandex_search.get_search_link_by_url(image_url),
        }


async def general_image_search(bot: Bot, update: Update, image_file, image_extension: str = None):
    """Send reverse image search links."""
    search_handler = ReverseImageSearchHandler()
    search_links = await search_handler.search_image(image_file, image_extension)

    button_list = [
        [InlineKeyboardButton(text='IQDB', url=search_links['iqdb_url'])],
        [InlineKeyboardButton(text='Google', url=search_links['google_url'])],
        [InlineKeyboardButton(text='TinEye', url=search_links['tineye_url'])],
        [InlineKeyboardButton(text='Bing', url=search_links['bing_url'])],
        [InlineKeyboardButton(text='Yandex', url=search_links['yandex_url'])],
    ]

    reply_markup = InlineKeyboardMarkup(button_list)
    await update.message.reply_text(
        text='Search results:',
        reply_markup=reply_markup
    )


async def callback_best_match(update: Update, context: CallbackContext):
    """Find the best matches for an image based on a callback query."""
    await context.bot.answer_callback_query(update.callback_query.id, show_alert=False)
    url = update.callback_query.data.split(' ')[1]
    await best_match(update, context, [url])


async def best_match(update: Update, context: CallbackContext, args: list):
    """Find the best match for an image."""
    if not args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='You have to provide a URL to make this work.')
        return
    try:
        tineye = TinEyeReverseImageSearchEngine()
        iqdb = IQDBReverseImageSearchEngine()
        tineye.search_url = args[0]
        iqdb.search_url = args[0]

        chat_id = update.effective_chat.id
        message = await context.bot.send_message(chat_id, 'Searching for the best match on TinEye...')

        match = tineye.best_match
        if not match:
            await context.bot.edit_message_text(
                text='Nothing found on TinEye, searching on IQDB...',
                chat_id=chat_id,
                message_id=message.message_id
            )
            match = iqdb.best_match

        if match:
            reply = (
                'Best Match:\n'
                'Link: [{website_name}]({website})\n'.format(
                    website_name=match['website_name'],
                    website=match['website'],
                )
            )
            reply += dict_to_str(match, ignore=['website_name', 'website', 'image_url', 'thumbnail'])

            image_url = match.get('image_url', None) or match.get('website', None)
            thumbnail = match.get('image_url', None) or match.get('thumbnail', None)

            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Open', url=image_url)]])
            await context.bot.delete_message(chat_id, message.message_id)

            await context.bot.send_photo(chat_id=chat_id, photo=thumbnail)
            await context.bot.send_message(
                chat_id=chat_id,
                text=reply,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await context.bot.edit_message_text(
                text='Nothing found on TinEye nor IQDB.',
                chat_id=chat_id,
                message_id=message.message_id,
            )

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'An error occurred: {str(e)}')


async def unknown(update: Update, context: CallbackContext):
    """Send an error message to the client if the entered command is unknown."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
