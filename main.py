import get_data
import google_map_api
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Handler, StringCommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location, KeyboardButton, ReplyKeyboardMarkup
import time
import logging
import json
import requests

all_station_info = []
all_station_availability = []
dep_cord = (1,1)
des_cord = (1,1)

des_keyword = ""
dep_keyword = ""
a = ""
b = ""
dep_yes = ""
dep_no = ""
des_yes = ""
des_no = ""
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)


get_data.write_all_station_info()
get_data.write_all_station_availability()

all_station_info = get_data.load_all_station_info()
all_station_availability = get_data.load_all_station_availability()


def location(bot, update):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    update.message.reply_text(current_pos)
    #position=current_pos
    
def start(bot ,update):
    callback_data=0
    #要不要手動輸入
    update.message.reply_text("Hi, 我是單車趴趴走, 給我出發地和目的地, 我就可以分別幫你找到離這兩個地點最近且可用的ubike站點, 並發送導航網址給你喔😉")
    keyboard = [[InlineKeyboardButton("現在位置", callback_data='1'),
                 InlineKeyboardButton("其他位置", callback_data='0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('請輸入出發地位置\n您可以選擇使用現在位置或輸入其他地點', reply_markup=reply_markup)
    
    
def ask_dep(bot, update):
    global a

    callback_data = update.callback_query.data
    if(callback_data=="1"):
        location_handler = MessageHandler(Filters.location, location, edited_updates=True)
        updater.dispatcher.add_handler(location_handler)

    else:
        #手動enter location
        a = MessageHandler(Filters.text, dep_text)
        update.callback_query.edit_message_text("請輸入出發地的關鍵字（名稱、地址、經緯度）")
        updater.dispatcher.add_handler(a)


def dep_text(bot,update):
    global dep_cord, dep_keyword, a, dep_yes, dep_no, des_yes, des_no
    updater.dispatcher.remove_handler(des_yes)
    updater.dispatcher.remove_handler(des_no)
    updater.dispatcher.remove_handler(a)
    dep_keyword = update.message.text
    dep_cord = google_map_api.google_map_api(dep_keyword)
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    update.message.reply_location(dep_cord[0], dep_cord[1])
    yes = KeyboardButton("/是",False, False)
    no = KeyboardButton("/否")

    reply_keyboard_markup = ReplyKeyboardMarkup([[yes],[no]])

    update.message.reply_text("出發地是否正確", reply_markup=reply_keyboard_markup)
    dep_yes = CommandHandler("是", ask_des)
    dep_no = CommandHandler("否", start)
    updater.dispatcher.add_handler(dep_yes)
    updater.dispatcher.add_handler(dep_no)

def ask_des(bot, update):
    global b, dep_yes, dep_no
    updater.dispatcher.remove_handler(dep_yes)
    updater.dispatcher.remove_handler(dep_no)
    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）")
    b = MessageHandler(Filters.text, des_text)
    updater.dispatcher.add_handler(b)

def des_text(bot, update):
    global des_cord, des_keyword, b, des_yes, des_no
    updater.dispatcher.remove_handler(b)
    des_keyword = update.message.text
    des_cord = google_map_api.google_map_api(des_keyword)
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    update.message.reply_location(des_cord[0], des_cord[1])
    yes1 = KeyboardButton("/是")
    no1 = KeyboardButton("/否")

    reply_keyboard_markup1 = ReplyKeyboardMarkup([[yes1],[no1]])

    des_yes = CommandHandler("是", ubike_check)
    des_no = CommandHandler("否", ask_des)
    update.message.reply_text("目的地是否正確", reply_markup=reply_keyboard_markup1)
    updater.dispatcher.add_handler(des_yes)
    updater.dispatcher.add_handler(des_no)

    
def ubike_check(bot, update):
    global all_station_availability, all_station_info, dep_cord, des_cord, des_no, dep_yes
    updater.dispatcher.remove_handler(dep_yes)
    updater.dispatcher.remove_handler(dep_no)
    dep_bike = get_data.search(all_station_availability, all_station_info, dep_cord, 1)
    des_bike = get_data.search(all_station_availability, all_station_info, des_cord, 0)

    route = "{}➡️{}➡️{}➡️{}".format(dep_keyword, dep_bike["name"], des_bike["name"], des_keyword)
    update.message.reply_text("🗺️路線：")
    update.message.reply_text(route)
    url = get_data.get_direction_url(dep_keyword, dep_bike["cord"], des_bike["cord"], des_keyword)
    header = {"Content-Type":"application/json", "reurl-api-key":"4070df69d794e53c114b353100ba214de3d6b7398d894494ab38acc62b055f6689"}
    data = {"url": url}
    
    r = requests.post("https://api.reurl.cc/shorten", headers=header, data=json.dumps(data))
    update.message.reply_text("🧭導航網址：")
    update.message.reply_text(r.json()["short_url"])
    
    update.message.reply_text(" 🚲 站點資訊：")
    update.message.reply_text("▶️{}（借車站）\n目前車輛數目：{}".format(dep_bike["name"], dep_bike["bike"]))
    update.message.reply_text("▶️{}（還車站）\n目前空位數目：{}".format(des_bike["name"], des_bike["bike"]))
    update.message.reply_text("新的路線？")
    update.message.reply_text("/start")

updater = Updater("939455253:AAFQShx9QZ2WU31POxnGeeHyfuKJp73C3Lk")
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(ask_dep))


updater.start_polling()
updater.idle()