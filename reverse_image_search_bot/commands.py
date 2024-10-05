import io
import os
from tempfile import NamedTemporaryFile
from uuid import uuid4

from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip

from telegram.constants import ParseMode
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from reverse_image_search_bot.utils import dict_to_str
from .image_search import BingReverseImageSearchEngine, \
    GoogleReverseImageSearchEngine, IQDBReverseImageSearchEngine, \
    TinEyeReverseImageSearchEngine, YandexReverseImageSearchEngine


async def start(update: Update, context: CallbackContext):
    """Send Start / Help message to client.

    Args:
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
        context (:obj:`telegram.ext.CallbackContext`): Telegram Api Callback Context Object
    """
    reply = """*ReVot - Reverse Image Search Bot (MS AZURE)*

(Currently for testing not active all time, you know it's costly ;p)

*How to use me*
Send me images or stickers and I will send you direct reverse image search links for IQDB, Google, TinEy, Yandex and Bing.

*Commands*
- /help, /start: show a help message with information about the bot and it's usage.

Thank you for using.
(cosmos)
"""

    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply, parse_mode=ParseMode.MARKDOWN)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    image_dir = os.path.join(current_dir, 'images/example_usage.png')

    if os.path.exists(image_dir):
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_dir, 'rb'), caption='Example Usage')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Example image not found.')


def group_image_reply_search(bot: Bot, update: Update):
    """Reverse search for reply mentions to images in groups

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    print(update.message.reply_to_message.document.file_id)
    pass


def gif_image_search(bot: Bot, update: Update):
    """Send a reverse image search link for the GIF sent to us

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    update.message.reply_text('Please wait for your results ...')
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    document = update.message.document or update.message.video
    video = bot.getFile(document.file_id)

    with NamedTemporaryFile() as video_file:
        video.download(out=video_file)
        video_clip = VideoFileClip(video_file.name, audio=False)

        with NamedTemporaryFile(suffix='.gif') as gif_file:
            video_clip.write_gif(gif_file.name)

            dirname = os.path.dirname(gif_file.name)
            file_name = os.path.splitext(gif_file.name)[0]
            compressed_gif_path = os.path.join(dirname, file_name + '-min.gif')

            os.system('gifsicle -O3 --lossy=50 -o {dst} {src}'.format(dst=compressed_gif_path, src=gif_file.name))
            if os.path.isfile(compressed_gif_path):
                general_image_search(bot, update, compressed_gif_path, 'gif')
            else:
                general_image_search(bot, update, gif_file.name, 'gif')


def sticker_image_search(bot: Bot, update: Update):
    """Send a reverse image search link for the image of the sticker sent to us

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    update.message.reply_text('Please wait for your results ...')
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    sticker_image = bot.getFile(update.message.sticker.file_id)
    converted_image = io.BytesIO()

    with io.BytesIO() as image_buffer:
        sticker_image.download(out=image_buffer)
        with io.BufferedReader(image_buffer) as image_file:
            pil_image = Image.open(image_file).convert("RGBA")
            pil_image.save(converted_image, 'png')

            general_image_search(bot, update, converted_image, 'png')


async def image_search_link(update: Update, context: CallbackContext):
    """Send a reverse image search link for the image he sent us to the client

    Args:
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
        context (:obj:`telegram.ext.CallbackContext`): Telegram Api Callback Context Object
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Please wait for your results ...')

    if update.effective_message.photo:
        photo = update.effective_message.photo[-1]
    elif update.effective_message.document:
        photo = update.effective_message.document
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='No image found.')
        return

    file = await photo.get_file()
    image_buffer = io.BytesIO()
    await file.download_to_memory(destination=image_buffer)
    image_buffer.seek(0)
    with io.BufferedReader(image_buffer) as image_file:
        await general_image_search(context.bot, update, image_file)


def general_image_search(bot: Bot, update: Update, image_file, image_extension: str=None):
    """Send a reverse image search link for the image sent to us

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
        image_file: File like image to search for
        image_extension (:obj:`str`): What extension the image should have. Default is 'jpg'
    """
    image_extension = image_extension or 'jpg'

    iqdb_search = IQDBReverseImageSearchEngine()
    google_search = GoogleReverseImageSearchEngine()
    tineye_search = TinEyeReverseImageSearchEngine()
    bing_search = BingReverseImageSearchEngine()
    yandex_search = YandexReverseImageSearchEngine()

    image_url = iqdb_search.upload_image(image_file, 'irs-' + str(uuid4())[:8] + '.' + image_extension)

    iqdb_url = iqdb_search.get_search_link_by_url(image_url)
    google_url = google_search.get_search_link_by_url(image_url)
    tineye_url = tineye_search.get_search_link_by_url(image_url)
    bing_url = bing_search.get_search_link_by_url(image_url)
    yandex_url = yandex_search.get_search_link_by_url(image_url)

    button_list = [[
        InlineKeyboardButton(text='Best Match', callback_data='best_match ' + image_url)
    ], [
        InlineKeyboardButton(text='Go To Image', url=image_url)
    ], [
        InlineKeyboardButton(text='IQDB', url=iqdb_url),
        InlineKeyboardButton(text='GOOGLE', url=google_url),
    ], [
        InlineKeyboardButton(text='TINEYE', url=tineye_url),
        InlineKeyboardButton(text='BING', url=bing_url),
    ], [
        InlineKeyboardButton(text='YANDEX', url=yandex_url),
    ]]

    reply = 'You can either use "Best Match" to get your best match right here or search for yourself.'
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text(
        text=reply,
        reply_markup=reply_markup
    )


def callback_best_match(bot: Bot, update: Update):
    """Find best matches for an image for a :class:`telegram.callbackquery.CallbackQuery`.

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    bot.answer_callback_query(update.callback_query.id, show_alert=False)
    url = update.callback_query.data.split(' ')[1]
    best_match(bot, update, [url, ])


def best_match(bot: Bot, update: Update, args: list):
    """Find best matches for an image.

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
        args (:obj:`list`): List of arguments passed by the user
    """
    if not args:
        update.message.reply_text('You have to give me an URL to make this work.')
        return
    tineye = TinEyeReverseImageSearchEngine()
    iqdb = IQDBReverseImageSearchEngine()
    tineye.search_url = args[0]
    iqdb.search_url = args[0]

    chat_id = update.effective_chat.id
    message = bot.send_message(chat_id, 'Searching for best match on TinEye...')

    match = tineye.best_match
    if not match:
        bot.edit_message_text(
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

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text='Open', url=image_url), ], ])
        bot.delete_message(chat_id, message.message_id)

        bot.send_photo(chat_id=chat_id, photo=thumbnail)
        bot.send_message(
            chat_id=chat_id,
            text=reply,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        bot.edit_message_text(
            text='Nothing found on TinEye nor IQDB.',
            chat_id=chat_id,
            message_id=message.message_id,
        )


def unknown(bot: Bot, update: Update):
    """Send a error message to the client if the entered command did not work.

    Args:
        bot (:obj:`telegram.bot.Bot`): Telegram Api Bot Object.
        update (:obj:`telegram.update.Update`): Telegram Api Update Object
    """
    update.message.reply_text("Sorry, I didn't understand that command.")
