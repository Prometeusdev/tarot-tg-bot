import os
import logging
import random
import tg_analytic
import flask

from dotenv import load_dotenv
from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          CallbackQueryHandler, Filters, ConversationHandler)

from data.dictionaries import yes_no_dict, info_card_dict


server = flask.Flask(__name__)

load_dotenv()

PORT = int(os.environ.get('PORT', 5000))

secret_token = os.getenv('TOKEN')
admin_id = os.getenv('ID')
APP_NAME = os.getenv('APP_NAME')

FIRST, SECOND = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_yes_or_no(update, context):
    chat = update.effective_chat
    deck = 'Таро Уэйта'
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
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
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                     resize_keyboard=True)
    number_card = get_new_image(deck)
    answer = info_card_dict[number_card[0]]
    if chat.type == 'private':
        context.bot.send_photo(
            chat.id,
            number_card[1],
            caption=f'{name}, Ваша карта дня!\n{answer}',
            reply_markup=button)
    else:
        context.bot.send_photo(
            chat.id,
            number_card[1],
            caption=f'Ваша карта дня!\n{answer}',
            reply_markup=button)
    return deck


def get_question(update, context):
    chat = update.effective_chat
    text = update.effective_message.text
    possible_commands = ['/yes_or_no', 'вопрос', 'да', 'нет', 'да-нет']
    if text in possible_commands:
        text = 'Запрос Да-нет'
    tg_analytic.statistics(chat.id, text)
    button = ReplyKeyboardMarkup([['Сбудется ли моё желание?']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Задайте вопрос со знаком вопроса в конце предложения, или '
              'мысленно загадайте своё желание и воспользуйтесь кнопкой'),
        reply_markup=button)


def deck_selection(update, context):
    chat = update.effective_chat
    text = update.effective_message.text
    possible_commands = ['/card_of_the_day', 'выбрать колоду', 'колода',
                         'дай карту']
    if text in possible_commands:
        text = 'Запрос карты дня'
    tg_analytic.statistics(chat.id, text)
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
    text = update.effective_message.text
    possible_commands = ['/tarot_layout', 'полный расклад', 'услуги',
                         'расклады таро', 'запись на консультацию',
                         'консультация']
    if text in possible_commands:
        text = 'Запрос полного расклада'
    tg_analytic.statistics(chat.id, text)
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
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
    text = update.effective_message.text
    possible_commands = ['/author', 'автор', 'разработчик', 'админ']
    if text in possible_commands:
        text = 'Запрос автора'
    tg_analytic.statistics(chat.id, text)
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
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
    text = update.effective_message.text
    possible_commands = ['/help', 'помощь', 'help', 'хелп']
    if text in possible_commands:
        text = 'Запрос полного расклада'
    tg_analytic.statistics(chat.id, text)
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
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


def get_format(update, context):
    chat = update.effective_chat
    if str(chat.id) == admin_id:
        keyboard = [
            [
                InlineKeyboardButton('Команды', callback_data='команды'),
                InlineKeyboardButton('Пользователи',
                                     callback_data='пользователи')
            ],
            [InlineKeyboardButton('Пользователи команды',
                                  callback_data='пользователи команды')],
            [InlineKeyboardButton('Статистика в файле .txt',
                                  callback_data='тхт')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите формат статистики',
                                  reply_markup=reply_markup)
        return FIRST
    else:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                     resize_keyboard=True)
        context.bot.send_message(
            chat_id=chat.id,
            text=('У вас нет прав 😋'),
            reply_markup=button
            )


def number_of_days(update, _):
    query = update.callback_query
    if query.data == 'тхт':
        format = 'пользователи команды тхт'
    else:
        format = query.data
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton('1', callback_data=f'1 {format}'),
            InlineKeyboardButton('2', callback_data=f'2 {format}'),
            InlineKeyboardButton('3', callback_data=f'3 {format}'),
        ],
        [
            InlineKeyboardButton('4', callback_data=f'4 {format}'),
            InlineKeyboardButton('5', callback_data=f'5 {format}'),
            InlineKeyboardButton('6', callback_data=f'6 {format}'),
        ],
        [
            InlineKeyboardButton('7', callback_data=f'7 {format}'),
            InlineKeyboardButton('8', callback_data=f'8 {format}'),
            InlineKeyboardButton('9', callback_data=f'9 {format}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Выберите количество дней',
                            reply_markup=reply_markup)
    return SECOND


def get_statistics(update, context):
    chat = update.effective_chat
    query = update.callback_query
    answer = query.data
    query.answer()
    text = (f'статистика {answer}')
    st = text.split(' ')
    if 'txt' in st or 'тхт' in st:
        tg_analytic.analysis(st)
        with open('Статистика.txt', 'r', encoding='UTF-8') as file:
            context.bot.send_document(chat.id, file)
            tg_analytic.remove()
    else:
        messages = tg_analytic.analysis(st)
        context.bot.send_message(chat.id, messages)
    query.edit_message_text(text="Будет нужна ещё статистика, пиши!")
    return ConversationHandler.END


def get_start(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    text = update.effective_message.text
    tg_analytic.statistics(chat.id, text)
    if str(chat.id) == admin_id:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет'], ['Статистика']],
                                     resize_keyboard=True)
    else:
        button = ReplyKeyboardMarkup([['Карта дня', 'Да-нет']],
                                     resize_keyboard=True)
    print(chat.type)
    if chat.type == 'private':
        context.bot.send_message(
            chat_id=chat.id,
            text=('Привет, {}! Хотите узнать, что тебя сегодня ждёт?\n'
                  'Выберите для начала колоду и Вам выпадет карта '
                  'дня. Так же можете получить ответ \"да-нет\" на вопрос '
                  'на Ваше желание').format(name),
            reply_markup=button
            )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text=('Привет! Хотите узнать, что тебя сегодня ждёт?\n'
                  'Выберите для начала колоду и Вам выпадет карта '
                  'дня. Так же можете получить ответ \"да-нет\" на вопрос '
                  'на Ваше желание'),
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
    list_how = ['как дела', 'как настроение', 'как поживаешь', 'как жизнь']
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
        if chat.type == 'private':
            context.bot.send_message(
                chat_id=chat.id,
                text=list_hi_answer[random.randint(0, len(list_hi_answer)-1)],
                reply_markup=button
                )
        else:
            context.bot.send_message(
                chat_id=chat.id,
                text='Привет 👋',
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
    elif text[:10] == 'статистика':
        if str(chat.id) == admin_id:
            st = text.split(' ')
            if 'txt' in st or 'тхт' in st:
                tg_analytic.analysis(st)
                with open('Статистика.txt', 'r', encoding='UTF-8') as file:
                    context.bot.send_document(chat.id, file)
                    tg_analytic.remove()
            else:
                messages = tg_analytic.analysis(st)
                context.bot.send_message(chat.id, messages)
        else:
            context.bot.send_message(
                chat.id,
                'У вас нет прав 😋')
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
            if chat.type == 'private':
                context.bot.send_message(
                    chat_id=chat.id,
                    text=('{}, я Вас не понимаю 🤔, Попробуйте воспользоваться '
                          'меню команд.').format(name),
                    reply_markup=button
                    )
            else:
                context.bot.send_message(
                    chat_id=chat.id,
                    text=('Я Вас не понимаю 🤔, Попробуйте воспользоваться '
                          'меню команд.'),
                    reply_markup=button
                    )


@server.route('/' + secret_token, methods=['POST'])
def get_message():
    updater = Updater(token=secret_token)
    updater.bot.process_new_updates([updater.bot.de_json(
         flask.request.stream.read().decode("utf-8"))])
    return "!", 200

 
@server.route('/', methods=["GET"])
def webhook():
    updater = Updater(token=secret_token)
    updater.bot.remove_webhook()
    url = "https://{}.herokuapp.com/{}".format(APP_NAME, secret_token)
    updater.bot.setWebhook(url=url)
    return "Hello from Heroku!", 200


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

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Статистика'), get_format)],
        states={
            FIRST: [
                CallbackQueryHandler(number_of_days),
            ],
            SECOND: [
                CallbackQueryHandler(get_statistics),
            ],
        },
        fallbacks=[CommandHandler('start', get_start)],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, another_words))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=secret_token,
                          webhook_url=('https://tarot-helen-bot.herokuapp.com/'
                                       + secret_token))
    # updater.idle()


if __name__ == '__main__':
    main()
    server.run(host='0.0.0.0', port=PORT)
