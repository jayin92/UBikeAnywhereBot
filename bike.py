from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from geopy.geocoders import Nominatim
#import startfuc
#import locationfuc
import random, os
import logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
#MessageHandler(Filters.text, say_something)

p=0
position=()
deatination=()

def location(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    update.message.reply_text(current_pos)
    #position=current_pos
    print(current_pos)

def start(bot ,update):
    callback_data=0
    #要不要手動輸入
    keyboard = [[InlineKeyboardButton("現在位置", callback_data='1'),
                 InlineKeyboardButton("其他地點", callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('請輸入出發地位置\n您可以選擇使用現在位置或輸入其他地點', reply_markup=reply_markup)
    
    
def ask_dep(bot, update):
    callback_data = update.callback_query.data
    if(callback_data=="1"):
        location_handler = MessageHandler(Filters.location, location, edited_updates=True)
        updater.dispatcher.add_handler(location_handler)

    else:
        #手動enter location
        update.callback_query.edit_message_text("請輸入出發地的關鍵字（名稱、地址、經緯度）")
        updater.dispatcher.add_handler(MessageHandler(Filters.text, dep_text))

def dep_text(bot,update):
    


updater = Updater("905272267:AAELvWp5b4SGt--CQRuuXQKHCxgNRz_M7lQ")
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(askDep))

updater.start_polling()
updater.idle()