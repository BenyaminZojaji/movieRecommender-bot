import telebot
from recSys import Rec_sys

rs = Rec_sys()
TOKEN = '5238219897:AAGaJ9uvm_wk2m68dWZnDB0znbIRB7qciC4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_func(message):
	bot.send_message(message.chat.id,'Welcome ' + (message.chat.first_name) + '!😊\n/movie -Suggest you movies🍿\n/help -SOS!💬')

@bot.message_handler(commands=['movie'])
def movie(m):
    msg = bot.send_message(m.chat.id, 'give me at least 3 movie and your rating.😍🎬\n\nexample:\nPulp Fiction-5\nAkira-4.5\nJumanji-2\n\nNOTE: make sure to split movie\'s name and rate with - \nNOTE: Our database is incomplete We have movies until 2018')
    bot.register_next_step_handler(msg, mv1)
def mv1(m):
    bot.send_message(m.chat.id, f'{rs.recommender_system(m.text)}')

@bot.message_handler(commands=['help'])
def help_func(message):
	bot.reply_to(message, '/movie -Suggest you movies based on your rating!🎬🍿\n\nFor any issues pls contact my creator.\nbenyamin.zojaji@gmail.com')
bot.polling(none_stop=True)