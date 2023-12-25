# -*-coding:utf8;-*-
from bottle import route, request, post
from mybot.pustaka import db
import bottle
import telebot
import os
import chatrouter
import mybot


TOKEN = os.environ.get("TG_BOT_TOKEN", "INSERT YOUR BOT TOKEN HERE")
HOST = os.environ.get("TG_BOT_HOST", "INSERT YOUR BOT HOST HERE")
bot = telebot.TeleBot(TOKEN)


@route('/')
def root_handler():
    return "its works!"


@route("/update_webhook")
def update_handler():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://{HOST}/{TOKEN.replace(":","_")}')
    return "OK"


@post('/'+TOKEN.replace(":", "_"))
def telegram_hook():
    data = request.body.read().decode("utf-8")
    update = telebot.types.Update.de_json(data)
    bot.process_new_updates([update])
    return "OK"


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    user_id = message.from_user.id
    chatrouter.data_user = message
    if not db.user_exists(user_id):
        db.add_user(user_id)
    session = db.get_user_session(user_id)
    r = chatrouter.run(chatrouter.group(session), message.text)
    if r is not None:
        bot.reply_to(message, r)


bottle.debug(True)
app = application = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=8080, debug=True)
