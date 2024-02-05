from flask import Flask, json, request
import telebot
import logging
import git

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('uniqueizercreo')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

@app.route('/')
def hello_world():
    return 'Hello New World 9!'
    
bot = telebot.TeleBot('6488073582:AAFD6MbpEMaJgRL1Zj1dBCxSKpSIa8AGEH4')    
    
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🖼 Уникализировать картинку")
    bot.send_message(message.chat.id, "👋 Добро пожаловать в бот для уникализации картинок от команды Усатого Арбитражника!\n\n"
                                      "🚀 В будущем мы будем дорабатывать этот проект и добавлять много полезных функций!\n\n"
                                      "⚠️ Прежде чем начать подпишись на YouTube канал автора - https://www.youtube.com/@usaffiliate\n\n"
                                      "📣 Также, подпишись на Telegram канал автора - @mustage_affiliate\n\n"
                                      "💬 А если у тебя нет друзей, тебе грустно и одиноко или же у тебя у тебя есть вопросы на которые тебе нужны ответы, то мы будем рады видеть тебя в нашем telegram чате - https://t.me/+eMzWlE9neiY2ZjEy\n\n"
                                      "⬇️ Чтобы уникализировать изображение просто нажми на кнопку ниже.", reply_markup=markup) 

bot.polling()                                      