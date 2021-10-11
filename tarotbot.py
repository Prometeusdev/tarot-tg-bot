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


deck = 'Basic_Waite_Tarot'


def get_deck(message):
    print(message)
    decks = {
        'Basic_Waite_Tarot': '/Basic_Waite_Tarot',
        'Animals_Divine_Tarot': '/Animals_Divine_Tarot',
        'Alkhimicheskoe_taro': '/Alkhimicheskoe_taro',
        'Tarot_of_Casanova': '/Tarot_of_Casanova',
    }
    try:
        if message in decks.items:
            deck = decks.key[message]
    except Exception as error:
        logging.error(f'Такой колоды не существует: {error}')
        deck = 'Basic_Waite_Tarot'
    return deck


def deck_selection(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([
        ['/Basic_Waite_Tarot', '/Animals_Divine_Tarot'],
        ['/Alkhimicheskoe_taro', '/Tarot_of_Casanova']
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите колоду',
        reply_markup=button)
    return 

def get_new_image():
    random_number = random.randint(0,77)
    try:
        random_card = open(f'static/images/{deck}/{random_number}.JPG', 'rb')
    except Exception as error:
        logging.error(f'Ошибка в расположении картинки: {error}')
        random_card = open(f'static/images/Basic_Waite_Tarot/back.JPG', 'rb')
    return random_card


def new_card(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcard', '/decks']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}! Хочешь узнать, что тебя сегодня ждёт?'.format(name),
        reply_markup=button
        )


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, get_deck(Filters.text)))
    updater.dispatcher.add_handler(CommandHandler(f'{deck}', wake_up))
    updater.dispatcher.add_handler(CommandHandler('decks', deck_selection))
    updater.dispatcher.add_handler(CommandHandler('newcard', new_card))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
