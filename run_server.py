import flask
import os

from dotenv import load_dotenv
from telegram.ext import Updater

from tarotbot import main


server = flask.Flask(__name__)

load_dotenv()

TOKEN = os.getenv('TOKEN')
APP_NAME = os.getenv('APP_NAME')
PORT = int(os.environ.get('PORT', 80))

 
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    updater = Updater(token=TOKEN)
    updater.bot.process_new_updates([updater.bot.de_json(
         flask.request.stream.read().decode("utf-8"))])
    return "!", 200

 
@server.route('/', methods=["GET"])
def index():
    updater = Updater(token=TOKEN)
    url = "https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=url)
    updater.bot.setWebhook(url=url)
    return "Hello from Heroku!", 200


main()


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
