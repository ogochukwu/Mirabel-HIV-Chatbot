import telebot
from time import sleep
from list import *
from telebot import types

bot = telebot.TeleBot('1257796339:AAEwFZBSg3KjgV_Qjh9hRdZ4m5zA5L7put0') #your api token, do not share it with anybody

#this class making inline kaybord
class KEYBORD:
    def __init__(self,listt):
        self.listt = listt

    def markup(self):
        inline = types.InlineKeyboardMarkup(row_width=1)
        lis = []
        for i in self.listt:
            btn = types.InlineKeyboardButton(a[i]['title'], callback_data=a[i]['title'])
            lis.append(btn)
        inline.add(*lis)
        return inline

#back keybord,
arrow = types.InlineKeyboardMarkup(row_width=1)
btn_arrow = types.InlineKeyboardButton(text='⬅️', callback_data='back')# you can change the icon just edit text = 'new emoji'
arrow.add(btn_arrow)

dicr = {}
dicr2 = {}

start_text = 'Hello, ask me something, and I\'ll try to give you good answers' #change start message
choose = 'Do you intend to ask?' # change choose message
sorry = 'Sorry, I do not understand your question, please rephrase.' #change sorry message


@bot.message_handler(commands=['start'])
def st(message):
    bot.send_message(message.chat.id, start_text)

#working with text message, and looking for right tags
@bot.message_handler(content_types=['text'])
def m(message):
    dicr[message.chat.id] = []
    for i in enumerate(a):
        lol = [i.replace(" ", "") for i in i[1]['tag'].split(',')]
        for tag in lol:
            if tag.lower() in message.text.lower():
                dicr[message.chat.id].append(i[0])
                dicr[message.chat.id] = [tn for tn in set(dicr[message.chat.id])]
    if len(dicr[message.chat.id]) == 0:
        bot.send_message(message.chat.id, sorry)
    else:
        bot.send_message(message.chat.id, choose, reply_markup=KEYBORD(dicr[message.chat.id]).markup())

#calling the tags and request the context
@bot.callback_query_handler(func=lambda call: True)
def c(call):
    if call.data == 'back':
        bot.answer_callback_query(callback_query_id=call.id)
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=choose,
                                  parse_mode='html',
                                  reply_markup=KEYBORD(dicr[call.message.chat.id]).markup())
        except:
            pass
    else:
        bot.answer_callback_query(callback_query_id=call.id)
        dicr2[call.message.chat.id] = []
        for i in enumerate(a):
            if call.data == i[1]['title']:
                dicr2[call.message.chat.id].append(i[0])
        data = a[dicr2[call.message.chat.id][0]]['content']
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=data,
                              parse_mode='html',
                              reply_markup=arrow)
        except:
            pass
#loop circle
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        sleep(15)
