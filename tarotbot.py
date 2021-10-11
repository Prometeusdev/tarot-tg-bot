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

PORT = int(os.environ.get('PORT', 80))
secret_token = os.getenv('TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_deck(update, context):
    text = update.effective_message.text
    chat = update.effective_chat
    try:
        deck = text
    except Exception as error:
        logging.error(f'Такой колоды не существует: {error}')
        deck = 'Таро Уэйта'
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
        ['Таро Уэйта', 'Таро Божественных Животных']
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Выберите колоду карт',
        reply_markup=button)


def get_new_image(deck):
    random_number = random.randint(0, 77)
    deck = deck
    try:
        random_card = open(f'static/images/{deck}/{random_number}.JPG', 'rb')
    except Exception as error:
        logging.error(f'Ошибка в расположении картинки: {error}')
        random_card = open('static/images/Таро Уэйта/back.JPG', 'rb')
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
        Filters.regex('Таро Уэйта') |
        Filters.regex('Таро Божественных Животных'), get_deck))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=secret_token,
                          webhook_url=('https://hellocowboybot.herokuapp.com/'
                                       + secret_token))
    #updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
