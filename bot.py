import config
import telebot
import logging
import sqlite3 as lite
from telebot import types

bot  = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'ask'])
def handle_start_help(message):

    markup = types.ReplyKeyboardMarkup()
    markup.row('matan')
    markup.row('geometry')
    msg = bot.send_message(message.chat.id, "Wat exam do u wanna pass?????", reply_markup=markup)
    bot.register_next_step_handler(msg, exam)
    
def exam(m):

    if m.text == 'matan':
        bot.send_message(m.chat.id, 'Here you go', reply_markup=types.ReplyKeyboardRemove())
        con = lite.connect('matan.db')
        kb  = types.InlineKeyboardMarkup()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM answers_exams")
            i = 1
            while True:
                row = cur.fetchone()

                if row == None:
                    break
                
                kb.add(types.InlineKeyboardButton(text = row[1], callback_data = i))
                i = i + 1
        bot.send_message (m.chat.id,"Feel free to choose, enter /ask to get answers on another exam", reply_markup=kb)
        con.close()
    elif m.text == 'geometry':
        bot.send_message(m.chat.id, 'Here u go', reply_markup=types.ReplyKeyboardRemove())
        con = lite.connect('matan.db')
        kb  = types.InlineKeyboardMarkup()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM answers_geom")
            i = 1
            while True:
                row = cur.fetchone()

                if row == None:
                    break
                
                kb.add(types.InlineKeyboardButton(text = row[1], callback_data = i+100))
                i = i + 1
        bot.send_message (m.chat.id,"Feel free to choose, honey, enter /ask to get answers on another exam", reply_markup=kb)
        con.close()
        
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    n = int(call.data)
    con  = lite.connect('matan.db')
    with con:
        cur  = con.cursor()
        if n<=100:
            cur.execute("SELECT * FROM answers_exams WHERE id=:element", {"element":n})
            row = cur.fetchone()
            bot.send_message(call.message.chat.id, row[1])
            bot.send_photo(call.message.chat.id, row[2])
        elif n>100:
            n = n - 100
            cur.execute("SELECT * FROM answers_geom WHERE id=:element", {"element":n})
            row = cur.fetchone()
            bot.send_message(call.message.chat.id, row[1])
            bot.send_photo(call.message.chat.id, row[2])
    con.close()
if __name__ == '__main__':
     bot.polling(none_stop=True)
     
