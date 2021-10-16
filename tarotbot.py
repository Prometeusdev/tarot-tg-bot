import os
import logging
import random

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


load_dotenv()

PORT = int(os.environ.get('PORT', 80))

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_yes_or_no(update, context):
    text = update.effective_message.text
    chat = update.effective_chat
    try:
        deck = text
    except Exception as error:
        logging.error(f'Такой колоды не существует: {error}')
        deck = 'Таро Уэйта'
    button = ReplyKeyboardMarkup([['/decks']],
                                 resize_keyboard=True)
    answer = get_new_image(deck)[0]
    try:
        file = open(f'/app/data/yes_or_no.txt', 'rb')
        answer = file[get_new_image(deck)[0]]
    except Exception as error:
        logging.error(f'Ошибка в расположении картинки: {error}')
        answer = 'Ответа пока нет'
    context.bot.send_photo(
        chat.id,
        get_new_image(deck)[1],
        caption='{}'.format(answer),
        reply_markup=button)
    return deck


def get_deck(update, context):
    text = update.effective_message.text
    chat = update.effective_chat
    name = update.message.chat.first_name
    try:
        deck = text
    except Exception as error:
        logging.error(f'Такой колоды не существует: {error}')
        deck = 'Таро Уэйта'
    button = ReplyKeyboardMarkup([['/decks']],
                                 resize_keyboard=True)
    context.bot.send_photo(
        chat.id,
        get_new_image(deck)[1],
        caption='{}, Ваша карта дня'.format(name),
        reply_markup=button)
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
        random_card = open(f'/app/media/images/{deck}/{random_number}.jpg',
                           'rb')
    except Exception as error:
        logging.error(f'Ошибка в расположении картинки: {error}')
        random_card = open('/app/media/images/Таро Уэйта/back.jpg', 'rb')
    return random_number, random_card


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


def another_words(update, context):
    text = update.effective_message.text.lower()
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/decks']],
                                 resize_keyboard=True)
    list_card = ['выбрать колоду', 'колода', 'карта дня', 'дай карту']
    list_hi = ['привет', 'здравствуй', 'здравствуйте', 'хай', 'хелло', '👋']
    list_how = ['как дела', 'как ты', 'как настроение', 'как поживаешь',
                'как жизнь']
    if text in list_card:
        deck_selection(update, context)
    elif [word for word in list_hi if word in text]:
        list_hi_answer = [
            '{}, привет, может погадаем?'.format(name),
            'Здравствуйте, {}!'.format(name),
            'Hello 👋',
            ]
        list_hi_sticker = [
            ('CAACAgIAAxkBAAIOo2FnFc3Eh9gzBko5fi-edLxZAAHqyAACVAADQbVWDGq3-McI'
             'jQH6IQQ'),
            ('CAACAgIAAxkBAAIOpWFnFmMMAp8nzN3Gv1rurTWmYeLuAAIRAwAC8-O-CxlunyW'
             'ezCwkIQQ'),
            ('CAACAgIAAxkBAAIOp2FnF4qCXJqteKd7YOAtiSyVyFZ4AAKSAQACVp29Cp_QLQ'
             'hCLtUFIQQ'),
            ('CAACAgIAAxkBAAIOqWFnGBi90XgL4WneLHIN2i7PF2KgAAI1AQACMNSdEbS4Nf1m'
             'oLZ8IQQ'),
        ]
        context.bot.send_message(
            chat_id=chat.id,
            text=list_hi_answer[random.randint(0, len(list_hi_answer)-1)],
            reply_markup=button
            )
        context.bot.send_sticker(
            chat.id,
            list_hi_sticker[random.randint(0, len(list_hi_sticker)-1)]
            )
    elif [word for word in list_how if word in text]:
        list_answer = ['У меня все прекрасно', 'Сейчас бы погадать 🔮',
                       'Хорошо', 'Радуюсь жизни 😍',
                       'Готов много работать 🤓', '👍']
        context.bot.send_message(
            chat_id=chat.id,
            text=list_answer[random.randint(0, len(list_answer)-1)],
            reply_markup=button
            )
    elif 'таролог' in text:
        context.bot.send_message(
            chat_id=chat.id,
            text='Елена Логинова, https://www.instagram.com/hellyloginson/ \n'
                 'ТАРО ✳️ Предсказания, полезные советы.'
                 'Отвечу на ваши вопросы',
            reply_markup=button
            )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text='{}, я Вас не понимаю, используйте меню команд'.format(name),
            reply_markup=button
            )


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', get_start))
    updater.dispatcher.add_handler(CommandHandler('decks', deck_selection))
    updater.dispatcher.add_handler(CommandHandler('yes_or_no',
                                                  deck_selection))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Таро Уэйта') |
        Filters.regex('Таро Божественных Животных'), get_deck))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, another_words))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=secret_token,
                          webhook_url=('https://tarot-helen-bot.herokuapp.com/'
                                       + secret_token))
    # updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
