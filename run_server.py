import os

from dotenv import load_dotenv
from flask import Flask, request
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          CallbackQueryHandler, Filters, ConversationHandler)

import tarotbot


server = Flask(__name__)

load_dotenv()

PORT = int(os.environ.get('PORT', 80))
secret_token = os.getenv('TOKEN')
admin_id = os.getenv('ID')
APP_NAME = os.getenv('APP_NAME')



def main():
    updater = Updater(token=secret_token)

    updater.dispatcher.add_handler(CommandHandler('start', tarotbot.get_start))
    updater.dispatcher.add_handler(CommandHandler('card_of_the_day',
                                                  tarotbot.deck_selection))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Карта дня'),
                                                  tarotbot.deck_selection))
    updater.dispatcher.add_handler(CommandHandler('yes_or_no',
                                                  tarotbot.get_question))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('Да-нет'),
                                                  tarotbot.get_question))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Таро Уэйта') |
        Filters.regex('Таро Божественных Животных'), tarotbot.get_deck))
    updater.dispatcher.add_handler(CommandHandler('tarot_layout',
                                                  tarotbot.get_tarot_layout))
    updater.dispatcher.add_handler(CommandHandler('help', tarotbot.get_help))
    updater.dispatcher.add_handler(CommandHandler('author',
                                                  tarotbot.get_author))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Статистика'),
                                     tarotbot.get_format)],
        states={
            tarotbot.FIRST: [
                CallbackQueryHandler(tarotbot.number_of_days),
            ],
            tarotbot.SECOND: [
                CallbackQueryHandler(tarotbot.get_statistics),
            ],
        },
        fallbacks=[CommandHandler('start', tarotbot.get_start)],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(MessageHandler(Filters.text,
                                                  tarotbot.another_words))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=secret_token,
                          webhook_url=('https://tarot-helen-bot.herokuapp.com/'
                                       + secret_token))
    updater.idle()


if __name__ == '__main__':
    main()
    server.run()
