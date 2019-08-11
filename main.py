import get_data
import google_map_api
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Handler, StringCommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
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



all_station_info = get_data.load_all_station_info()
all_station_availability = get_data.load_all_station_availability()



def location(bot, update, user_data):
    user_data["ask_dep"] = MessageHandler(Filters.text, dep_text, pass_user_data=True)

    user_data["dep_keyword"] = "現在位置"
    user_data["dep_cord"] = (update.message.location['latitude'], update.message.location['longitude'])

    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    user_data["ask_des"] = MessageHandler(Filters.text, des_text_current, pass_user_data=True)
    updater.dispatcher.add_handler(user_data["ask_des"])

def location_fix(bot, update, user_data):
    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    user_data["ask_des"] = MessageHandler(Filters.text, des_text_current, pass_user_data=True)
    updater.dispatcher.add_handler(user_data["ask_des"])

def des_text_current(bot, update, user_data):
    updater.dispatcher.remove_handler(user_data["ask_des"])
    user_data["des_keyword"] = update.message.text
    user_data["des_cord"] = google_map_api.google_map_api(user_data["des_keyword"])
    if(user_data["des_cord"] == "error"):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
        
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    else:
        updater.dispatcher.remove_handler(user_data["ask_des"])

        update.message.reply_location(user_data["des_cord"][0], user_data["des_cord"][1])
        yes1 = KeyboardButton("/是")
        no1 = KeyboardButton("/否")

        reply_keyboard_markup1 = ReplyKeyboardMarkup([[yes1],[no1]])

        user_data["des_yes"] = CommandHandler("是", ubike_check, pass_user_data=True)
        user_data["des_no"] = CommandHandler("否", location_fix, pass_user_data=True)
        update.message.reply_text("目的地是否正確", reply_markup=reply_keyboard_markup1)
        updater.dispatcher.add_handler(user_data["des_yes"])
        updater.dispatcher.add_handler(user_data["des_no"])

    
def start(bot ,update, user_data):
    if "des_yes" in user_data:
        updater.dispatcher.remove_handler(user_data["des_yes"])
    if "des_no" in user_data:
        updater.dispatcher.remove_handler(user_data["des_no"])
    if "dep_no" in user_data:
        updater.dispatcher.remove_handler(user_data["dep_no"])
    if "dep_yes" in user_data:
        updater.dispatcher.remove_handler(user_data["dep_yes"])




    get_data.write_all_station_info()
    get_data.write_all_station_availability()
    #要不要手動輸入
    now_location = KeyboardButton("/現在位置", False, True)
    other_location = KeyboardButton("/其他位置")

    keyboard = ReplyKeyboardMarkup([[now_location],[other_location]])
    update.message.reply_text("Hi, 我是單車趴趴走, 給我出發地和目的地, 我就可以分別幫你找到離這兩個地點最近且可用的ubike站點, 並發送導航網址給你喔😉")
    update.message.reply_text('請輸入出發地位置\n您可以選擇使用現在位置或輸入其他地點', reply_markup=keyboard)
    updater.dispatcher.add_handler(MessageHandler(Filters.location, location, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler("其他位置", ask_dep, pass_user_data=True))
    
    
def ask_dep(bot, update, user_data):
        #手動enter location
    user_data["ask_dep"] = MessageHandler(Filters.text, dep_text, pass_user_data=True)
    update.message.reply_text("請輸入出發地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    updater.dispatcher.add_handler(user_data["ask_dep"])


def dep_text(bot,update, user_data):
    global dep_cord, dep_keyword, a, dep_yes, dep_no, des_yes, des_no
    updater.dispatcher.remove_handler(user_data["ask_dep"])


    user_data["dep_keyword"] = update.message.text
    user_data["dep_cord"] = google_map_api.google_map_api(user_data["dep_keyword"])
    if(user_data["dep_cord"] == "error"):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    else:
        update.message.reply_location(user_data["dep_cord"][0], user_data["dep_cord"][1])
        yes = KeyboardButton("/是",False, False)
        no = KeyboardButton("/否")

        reply_keyboard_markup = ReplyKeyboardMarkup([[yes],[no]])

        update.message.reply_text("出發地是否正確", reply_markup=reply_keyboard_markup)
        user_data["dep_yes"] = CommandHandler("是", ask_des, pass_user_data=True)
        user_data["dep_no"] = CommandHandler("否", start, pass_user_data=True)
        updater.dispatcher.add_handler(user_data["dep_yes"])
        updater.dispatcher.add_handler(user_data["dep_no"])

def ask_des(bot, update, user_data):
    
    updater.dispatcher.remove_handler(user_data["dep_yes"])
    updater.dispatcher.remove_handler(user_data["dep_no"])
    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    user_data["ask_des"] = MessageHandler(Filters.text, des_text, pass_user_data=True)
    updater.dispatcher.add_handler(user_data["ask_des"])

def des_text(bot, update, user_data):
    if "ask_des" in user_data:
        updater.dispatcher.remove_handler(user_data["ask_des"])
    user_data["des_keyword"] = update.message.text
    user_data["des_cord"] = google_map_api.google_map_api(user_data["des_keyword"])
    if(user_data["des_cord"] == "error"):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
        
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    else:
        updater.dispatcher.remove_handler(user_data["ask_des"])

        update.message.reply_location(user_data["des_cord"][0], user_data["des_cord"][1])
        yes1 = KeyboardButton("/是")
        no1 = KeyboardButton("/否")

        reply_keyboard_markup1 = ReplyKeyboardMarkup([[yes1],[no1]])

        user_data["des_yes"] = CommandHandler("是", ubike_check, pass_user_data=True)
        user_data["des_no"] = CommandHandler("否", ask_des, pass_user_data=True)
        update.message.reply_text("目的地是否正確", reply_markup=reply_keyboard_markup1)
        updater.dispatcher.add_handler(user_data["des_yes"])
        updater.dispatcher.add_handler(user_data["des_no"])

    
def ubike_check(bot, update, user_data):
    updater.dispatcher.remove_handler(user_data["des_yes"] )
    updater.dispatcher.remove_handler(user_data["des_no"] )
    user_data["dep_bike"] = get_data.search(all_station_availability, all_station_info, user_data["dep_cord"], 1)
    user_data["des_bike"] = get_data.search(all_station_availability, all_station_info, user_data["des_cord"], 0)

    user_data["route"] = "{}➡️{}➡️{}➡️{}".format(user_data["dep_keyword"], user_data["dep_bike"]["name"], user_data["des_bike"]["name"], user_data["des_keyword"])
    update.message.reply_text("🗺️路線：", reply_markup=ReplyKeyboardRemove(True))
    update.message.reply_text(user_data["route"])
    url = get_data.get_direction_url(user_data["dep_cord"], user_data["dep_bike"]["cord"], user_data["des_bike"]["cord"], user_data["des_keyword"])
    user_data["header"] = {"Content-Type":"application/json", "reurl-api-key":"4070df69d794e53c114b353100ba214de3d6b7398d894494ab38acc62b055f6689"}
    user_data["data"] = {"url": url}
    data = {
        "dynamicLinkInfo": {
            "domainUriPrefix": "https://bikeanywhere.page.link",
            "link": url,
            "androidInfo": {
            "androidPackageName": "com.google.android.gms.maps",
            },
            "iosInfo": {
            "iosBundleId": "com.google.Maps",
            },
        },
        "suffix": {
            "option": "SHORT"
        }
    }
    
    api_url = url = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={}".format("AIzaSyD57zm-VEPud6YTbl6XKpu7kZIdlHxHZIQ")
    user_data["r"] = requests.post(api_url, data=json.dumps(data))
    
    update.message.reply_text("🧭導航網址：")
    update.message.reply_text(user_data["r"].json()["shortLink"])
    
    update.message.reply_text(" 🚲 站點資訊：")
    update.message.reply_text("▶️{}（借車站）\n目前車輛數目：{}".format(user_data["dep_bike"]["name"], user_data["dep_bike"]["bike"]))
    update.message.reply_text("▶️{}（還車站）\n目前空位數目：{}".format(user_data["des_bike"]["name"], user_data["des_bike"]["bike"]))
    update.message.reply_text("新的路線？")
    update.message.reply_text("/start")

updater = Updater("939455253:AAFQShx9QZ2WU31POxnGeeHyfuKJp73C3Lk")
updater.dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
updater.dispatcher.add_handler(CallbackQueryHandler(ask_dep, pass_user_data=True))


updater.start_polling()
updater.idle()