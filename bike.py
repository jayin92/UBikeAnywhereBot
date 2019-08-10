from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os,random

yes = KeyboardButton("現在位置",False, True)
no = KeyboardButton("其他位置")

reply_keyboard_markup = ReplyKeyboardMarkup([[yes],[no]])

start_lat = 0
start_lng = 0

stop_lat = 0
stop_lng = 0

def ask_location(bot, update):
    update.message.reply_text("請輸入其他位置", reply_markup=reply_keyboard_markup)

def start(bot, update):
    print("qwqw")
    update.message.reply_text("你要使用現在位置或其他位置？", reply_markup=reply_keyboard_markup)

def now_location(bot, update):

    print(update.message.location)
    start_lat = update.message.location['latitude']
    start_lng = update.message.location['longitude']


updater = Updater("970742110:AAHA5UXQWJDjYFJi_KNm84Umug4RcSMkCZE")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.location, now_location))
updater.dispatcher.add_handler(MessageHandler(Filters.text, other_location))


updater.start_polling()
updater.idle()