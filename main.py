import get_data
import google_map_api

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Handler, StringCommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import time
import logging
import json
import requests
import configparser
import time
# from notify_run import Notify

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

get_data.write_all_station_availability()
get_data.write_all_station_info()
last_update = time.time()

config = configparser.ConfigParser()
config.read('config.ini')

def info(update, context):
    info_str_1 = """
    API們：
    PTX API： 
    https://ptx.transportdata.tw/PTX/Service?categoryName=%E8%87%AA%E8%A1%8C%E8%BB%8A
    Google Maps API： 
    https://developers.google.com/maps/documentation/?hl=zh-tw
    Firebase Dynamic Links： 
    https://firebase.google.com/docs/dynamic-links
    """
    info_str_2 = """
    Github：
    https://github.com/jayin92/UBikeAnywhereBot
    """
    info_str_3 = """
    Developers：
    @jayinnn
    @kn71026
    @yuanqiuye
    @KJK0508
    @heartietehhy
    Max Pan
    資料介接「交通部PTX平臺」
    https://ptx.transportdata.tw/PTX/logo.png
    """
    update.message.reply_text(info_str_1)
    update.message.reply_text(info_str_2)
    update.message.reply_text(info_str_3)

def location(update, context):
    print(context.user_data)
    context.user_data["ask_dep"] = MessageHandler(Filters.text, dep_text, pass_user_data=True)

    context.user_data["dep_keyword"] = "現在位置"
    context.user_data["dep_cord"] = (update.message.location['latitude'], update.message.location['longitude'])

    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    context.user_data["ask_des"] = MessageHandler(Filters.text, des_text_current, pass_user_data=True)
    updater.dispatcher.add_handler(context.user_data["ask_des"])

def location_fix(update, context):
    print(context.user_data)

    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    context.user_data["ask_des"] = MessageHandler(Filters.text, des_text_current, pass_user_data=True)
    updater.dispatcher.add_handler(context.user_data["ask_des"])

def des_text_current(update, context):
    print(context.user_data)
    
    if "ask_des" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["ask_des"])
    context.user_data["des_keyword"] = update.message.text
    context.user_data["des_cord"] = google_map_api.google_map_api(context.user_data["des_keyword"])
    if(context.user_data["des_cord"] == "error"):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
        
    else:
        if "ask_des" in context.user_data:
            updater.dispatcher.remove_handler(context.user_data["ask_des"])

        update.message.reply_location(context.user_data["des_cord"][0], context.user_data["des_cord"][1])
        yes1 = KeyboardButton("/Yes")
        no1 = KeyboardButton("/No")

        reply_keyboard_markup1 = ReplyKeyboardMarkup([[yes1],[no1]])

        context.user_data["des_yes"] = CommandHandler("Yes", ubike_check, pass_user_data=True)
        context.user_data["des_no"] = CommandHandler("No", location_fix, pass_user_data=True)
        update.message.reply_text("目的地是否正確", reply_markup=reply_keyboard_markup1)
        updater.dispatcher.add_handler(context.user_data["des_yes"])
        updater.dispatcher.add_handler(context.user_data["des_no"])

    

def start(update, context):
    print(context.user_data)

    global last_update, all_station_info, all_station_availability
    # notify = Notify()
    user = update.message.from_user
    print(user["username"])
    # notify.send(user["username"])
    context.user_data.clear()
    if time.time() - last_update > 300:
        get_data.write_all_station_info()
        get_data.write_all_station_availability()
        last_update = time.time()

    all_station_info = get_data.load_all_station_info()
    all_station_availability = get_data.load_all_station_availability()
    
    # 要不要手動輸入
    now_location = KeyboardButton("/current", False, True)
    other_location = KeyboardButton("/other")

    keyboard = ReplyKeyboardMarkup([[now_location],[other_location]])
    update.message.reply_text("Hi, 我是單車趴趴走, 給我出發地和目的地, 我就可以分別幫你找到離這兩個地點最近且可用的ubike站點, 並發送導航網址給你喔😉")
    update.message.reply_text('請輸入出發地位置\n您可以選擇使用現在位置或輸入其他地點', reply_markup=keyboard)
    updater.dispatcher.add_handler(MessageHandler(Filters.location, location, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler("other", ask_dep, pass_user_data=True))
    
    
def ask_dep(update, context):
    print(context.user_data)

    # 手動enter location
    context.user_data["ask_dep"] = MessageHandler(Filters.text, dep_text, pass_user_data=True)
    update.message.reply_text("請輸入出發地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    updater.dispatcher.add_handler(context.user_data["ask_dep"])


def dep_text(update, context):
    print(context.user_data)

    global dep_cord, dep_keyword, a, dep_yes, dep_no, des_yes, des_no
    if "ask_dep" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["ask_dep"])


    context.user_data["dep_keyword"] = update.message.text
    context.user_data["dep_cord"] = google_map_api.google_map_api(context.user_data["dep_keyword"])
    if(context.user_data["dep_cord"] == "error"):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
    # update.message.reply_text(get_data.search(all_station_availability, all_station_info, cord, 1)["name"])
    else:
        update.message.reply_location(context.user_data["dep_cord"][0], context.user_data["dep_cord"][1])
        yes = KeyboardButton("/Yes",False, False)
        no = KeyboardButton("/No")

        reply_keyboard_markup = ReplyKeyboardMarkup([[yes],[no]])

        update.message.reply_text("出發地是否正確", reply_markup=reply_keyboard_markup)
        context.user_data["dep_yes"] = CommandHandler("Yes", ask_des, pass_user_data=True)
        context.user_data["dep_no"] = CommandHandler("No", start, pass_user_data=True)
        updater.dispatcher.add_handler(context.user_data["dep_yes"])
        updater.dispatcher.add_handler(context.user_data["dep_no"])

def ask_des(update, context):
    print(context.user_data)

    if "dep_yes" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["dep_yes"])
    if "dep_no" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["dep_no"])
    update.message.reply_text("請輸入目的地的關鍵字（名稱、地址、經緯度）", reply_markup=ReplyKeyboardRemove(True))
    context.user_data["ask_des"] = MessageHandler(Filters.text, des_text, pass_user_data=True)
    updater.dispatcher.add_handler(context.user_data["ask_des"])

def des_text(update, context):
    print(context.user_data)

    if "ask_des" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["ask_des"])
    context.user_data["des_keyword"] = update.message.text
    context.user_data["des_cord"] = google_map_api.google_map_api(context.user_data["des_keyword"])
    if(context.user_data["des_cord"] == "error" or context.user_data["des_cord"] == None):
        update.message.reply_text("❌找不到此地點")
        update.message.reply_text("重新開始？\n/start")
        updater.dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
        
    else:
        if "ask_des" in context.user_data:
            updater.dispatcher.remove_handler(context.user_data["ask_des"])

        update.message.reply_location(context.user_data["des_cord"][0], context.user_data["des_cord"][1])
        yes1 = KeyboardButton("/Yes")
        no1 = KeyboardButton("/No")

        reply_keyboard_markup1 = ReplyKeyboardMarkup([[yes1],[no1]])

        context.user_data["des_yes"] = CommandHandler("Yes", ubike_check, pass_user_data=True)
        context.user_data["des_no"] = CommandHandler("No", ask_des, pass_user_data=True)
        update.message.reply_text("目的地是否正確", reply_markup=reply_keyboard_markup1)
        updater.dispatcher.add_handler(context.user_data["des_yes"])
        updater.dispatcher.add_handler(context.user_data["des_no"])

    
def ubike_check(update, context):
    print(context.user_data)

    if "des_yes" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["des_yes"])
    if "des_no" in context.user_data:
        updater.dispatcher.remove_handler(context.user_data["des_no"] )
    context.user_data["dep_bike"] = get_data.search(all_station_availability, all_station_info, context.user_data["dep_cord"], 1)
    context.user_data["des_bike"] = get_data.search(all_station_availability, all_station_info, context.user_data["des_cord"], 0)

    context.user_data["route"] = "{}➡️{}➡️{}➡️{}".format(
        context.user_data["dep_keyword"], 
        context.user_data["dep_bike"]["name"], 
        context.user_data["des_bike"]["name"], 
        context.user_data["des_keyword"]
    )
    
    update.message.reply_text("🗺️路線：\n{}".format(context.user_data["route"]), reply_markup=ReplyKeyboardRemove(True))
    url = get_data.get_direction_url(
        context.user_data["dep_cord"], 
        context.user_data["dep_bike"]["cord"], 
        context.user_data["des_bike"]["cord"], 
        context.user_data["des_keyword"]
    )

    context.user_data["data"] = {"url": url}

    data = {
        "dynamicLinkInfo": {
            "domainUriPrefix": "https://ubikeanywhere.page.link",
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
    
    api_url = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?key={}".format(config["GOOGLE"]["APP_KEY"])
    context.user_data["r"] = requests.post(api_url, data=json.dumps(data))
    
    update.message.reply_text("🧭導航網址：{}".format(context.user_data["r"].json()["shortLink"]))    
    update.message.reply_text(" 🚲 站點資訊：\n{}\n{}".format("▶️{}（借車站）\n目前車輛數目：{}".format(
        context.user_data["dep_bike"]["name"], 
        context.user_data["dep_bike"]["bike"]), 
        "▶️{}（還車站）\n目前空位數目：{}".format(context.user_data["des_bike"]["name"], context.user_data["des_bike"]["bike"])
        ))
    update.message.reply_text("新的路線？\n/start")


    


if __name__ == '__main__':
    updater = Updater(config["TELEGRAM"]["ACCESS_TOKEN"], use_context=True) # use context based
    updater.dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
    updater.dispatcher.add_handler(CommandHandler('info', info))

    # updater.dispatcher.add_handler(CallbackQueryHandler(ask_dep, pass_user_data=True))


    updater.start_polling()
    updater.idle()