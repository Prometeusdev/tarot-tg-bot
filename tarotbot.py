import os
import logging
import random
# import tg_analytic

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from data.dictionaries import yes_no_dict, info_card_dict


load_dotenv()

PORT = int(os.environ.get('PORT', 80))

secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_yes_or_no(update, context):
    chat = update.effective_chat
    # text = update.effective_message.text
    # tg_analytic.analysis(chat.id, text)
    deck = 'Таро Уэйта'
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    number_card = get_new_image(deck)
    answer = yes_no_dict[number_card[0]]
    context.bot.send_photo(
        chat.id,
        number_card[1],
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
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    number_card = get_new_image(deck)
    answer = info_card_dict[number_card[0]]
    context.bot.send_photo(
        chat.id,
        number_card[1],
        caption=f'{name}, Ваша карта дня!\n{answer}',
        reply_markup=button)
    return deck


def get_question(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Сбудется ли моё желание?']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Задайте вопрос со знаком вопроса в конце предложения, или '
              'мысленно загадайте своё желание и воспользуйтесь кнопкой'),
        reply_markup=button)


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


def get_tarot_layout(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Расклады таро: на любовь, отношения, финансовое состояние, '
              'профессиональную сферу❤️💵\n'
              'Как обойти "острые углы"? Как избежать неприятностей?\n'
              'Я помогу Вам в этом разобраться!\n\n'
              'Запись на консультацию в чат @Lenoktaro\n'
              'Или в директ инстаграмма '
              'https://www.instagram.com/hellyloginson/\n'
              'Действует скидка 20% на первую консультацию по промокоду '
              '\"таро-бот\"'),
        reply_markup=button
        )


def get_author(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Привет, я Владимир!\nПрограммист, backend-разработчик 👨‍💻\n'
              'Написал бота для своей мамы.\n'
              'Надеюсь, этот бот и Вам пригодится.\n\n'
              'Нашли проблему? Чат @Rume73'),
        reply_markup=button
        )


def get_help(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Вы можете управлять мной, используя эти команды:\n'
              '/card_of_the_day - вытащить карту дня\n'
              '/yes_or_no - получить ответ "да-нет" на Ваше желание\n'
              '/tarot_layout - полный расклад\n'
              '/author - разработчик бота'),
        reply_markup=button
        )


def get_start(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
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
    button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                 resize_keyboard=True)
    list_card = ['выбрать колоду', 'колода', 'дай карту']
    list_yes_no = ['вопрос', 'да', 'нет', 'да-нет']
    list_help = ['помощь', 'help', 'хелп']
    list_author = ['автор', 'разработчик', 'админ']
    list_thanks = ['спасибо', 'благодарю', 'благодарствую', 'thank']
    list_tarot_layout = ['полный расклад', 'услуги', 'расклады таро',
                         'запись на консультацию', 'консультация']
    list_hi = ['привет', 'здравствуй', 'хай', 'хелло', '👋']
    list_how = ['как дела', 'как ты', 'как настроение', 'как поживаешь',
                'как жизнь']
    if text in list_yes_no:
        get_question(update, context)
    elif text in list_card:
        deck_selection(update, context)
    elif text[-1] == '?':
        get_yes_or_no(update, context)
    elif text in list_help:
        get_help(update, context)
    elif text in list_author:
        get_author(update, context)
    elif text in list_tarot_layout:
        get_tarot_layout(update, context)
    elif [word for word in list_thanks if word in text]:
        list_thanks_sticker = [
            ('CAACAgIAAxkBAAEDHy9hcIXrEYxTHtmeu2spfLrc05jU1wAC9wADVp29CgtyJB1I'
             '9A0wIQQ'),
            ('CAACAgIAAxkBAAEDHzNhcIYufGz2jIQsXRVIAlJK97RdkwACUgEAAjDUnRERwgZS'
             '_w81pCEE'),
            ('CAACAgIAAxkBAAEDHzVhcIZp1fyyTkf7-BbSi8uGr5QkswACLgkAAhhC7ghmx6Iw'
             'r7yx9CEE'),
            ('CAACAgEAAxkBAAEDHzdhcIbK3yNFllb94x81SRPMlcTydwAC6wEAAjgOghGzhgTO'
             '4ZxJOSEE'),
        ]
        context.bot.send_sticker(
            chat.id,
            list_thanks_sticker[random.randint(0, len(list_thanks_sticker)-1)]
            )
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
    elif text == 'таролог':
        context.bot.send_message(
            chat_id=chat.id,
            text='Елена Логинова, https://www.instagram.com/hellyloginson/\n'
                 'ТАРО ✳️ Предсказания, полезные советы.\n'
                 'Отвечу на ваши вопросы @Lenoktaro',
            reply_markup=button
            )
    # elif text == 'выведи статистику':
    #     st = text.split(' ')
    #     if 'txt' in st or 'тхт' in st:
    #         tg_analytic.analysis(st, chat.id)
    #         with open('%s.txt' %chat.id,'r',encoding='UTF-8') as file:
    #             context.send_document(chat.id, file)
    #             tg_analytic.remove(chat.id)
    #     else:
    #         messages = tg_analytic.analysis(st, chat.id)
    #         context.send_message(chat.id, messages)
    else:
        random_answer = random.randint(0, 2)
        if random_answer == 0:
            get_help(update, context)
        elif random_answer == 1:
            context.bot.send_sticker(
                chat.id,
                ('CAACAgIAAxkBAAEDHFxhbmwRWLa1ZySyHOeDfUFfcM4VQwACIQEAAvcCyA9E'
                 '9UdZozFIriEE'))
        else:
            context.bot.send_message(
                chat_id=chat.id,
                text=('{}, я Вас не понимаю 🤔, Попробуйте воспользоваться '
                      'меню команд.').format(name),
                reply_markup=button
                )


def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', get_start))
    updater.dispatcher.add_handler(CommandHandler('card_of_the_day',
                                                  deck_selection))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Карта дня'),
                                                  deck_selection))
    updater.dispatcher.add_handler(CommandHandler('yes_or_no',
                                                  get_question))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Да-нет'),
                                                  get_question))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Таро Уэйта') |
        Filters.regex('Таро Божественных Животных'), get_deck))
    updater.dispatcher.add_handler(CommandHandler('tarot_layout',
                                                  get_tarot_layout))
    updater.dispatcher.add_handler(CommandHandler('help', get_help))
    updater.dispatcher.add_handler(CommandHandler('author', get_author))
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
