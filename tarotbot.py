import os
import logging
import random

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

load_dotenv()

secret_token = os.getenv('TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_deck(update, context):
    text = update.effective_message.text
    chat = update.effective_chat
    try:
        deck = text[1:]
    except Exception as error:
        logging.error(f'Такой колоды не существует: {error}')
        deck = 'Basic_Waite_Tarot'
    button = ReplyKeyboardMarkup([['/decks']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=text,
        reply_markup=button
        )
    context.bot.send_photo(chat.id, get_new_image(deck))
    return deck


def deck_selection(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
        ['/Basic_Waite_Tarot', '/Animals_Divine_Tarot']
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите колоду',
        reply_markup=button)


def get_new_image(deck):
    random_number = random.randint(0, 77)
    deck = deck
    try:
        random_card = open(f'static/images/{deck}/{random_number}.JPG', 'rb')
    except Exception as error:
        logging.error(f'Ошибка в расположении картинки: {error}')
        random_card = open('static/images/Basic_Waite_Tarot/back.JPG', 'rb')
    return random_card


def get_start(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/decks']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Привет, {}! Хочешь узнать, что тебя сегодня ждёт?\n'
              'Выбери для начала колоду и Вам выпадет карта дня').format(name),
        reply_markup=button
        )


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', get_start))
    updater.dispatcher.add_handler(CommandHandler('decks', deck_selection))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('/Basic_Waite_Tarot') |
        Filters.regex('/Animals_Divine_Tarot'), get_deck))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
