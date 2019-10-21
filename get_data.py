# ptx app id:  839bc6f695d1479a83a04c0e7df512a1
# ptx app key: _Lm4jba4HpNdyXUpjNxgdiLmnlY 
# -*- coding: UTF-8 -*-

import configparser

import requests as req
import math
from ptxAuth import Auth 
from pprint import pprint
import json

def distance(loc1, loc2):
    """
    Function that calculate distance bewteen two locations

    Parameters:
        loc1 - first location coordinates (tuple)(Lat, Lon)
        loc2 - second location coordinates (tuple)(Lat, Lon)

    Returns:
        a float equal to distance between two locations
    """
    dy = loc1[0] - loc2[0]
    dx = loc1[1] - loc2[1]

    return dx**2 + dy**2


def get_direction_url(departure, station1, station2, destination):
    """
    Function that return google maps direction

    Parameters:
        departure: departue's name or address or coordinates
        station1: the station near departure, station's coordinates
        station2: the station near destination, station's coordinates
        destination: destination's name or address or coordinates
    """
    url = "https://www.google.com/maps/dir/?api=1&origin={}&destination={}&waypoints={}|{}&travelmode=walking".format(departure, destination, station1, station2)

    return url


def write_all_station_info():
    all_station_info = []
    for city in cities:
        url = "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/" + city + "/?$format=JSON"
        r = req.get(url, headers=a.get_auth_header())
        city_info = r.json()
        for station in city_info:
            all_station_info.append(station)

    js = json.dumps(all_station_info)

    with open("all_station_info.json", "w") as fp:
        fp.write(js)



def load_all_station_info():
    """
    Funtion that get station info data from ptx api and store infos in all_station_info list

    Parameters:
        all_station_info: a list store station info
    """
    with open("all_station_info.json", "r") as fp:
        all_station_info = json.load(fp)
    
    return all_station_info


def write_all_station_availability():
    all_station_availability = []
    for city in cities:
        url = "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/" + city + "/?$format=JSON"
        r = req.get(url, headers=a.get_auth_header())
        city_info = r.json()
        for station in city_info:
            all_station_availability.append(station)

    js = json.dumps(all_station_availability)

    with open("all_station_availability.json", "w") as fp:
        fp.write(js)
def load_all_station_availability():
    """
    Funtion that get station info data from ptx api and store infos in all_station_availability list

    Parameters:
        all_station_availability: a list store station availability
    """
    with open("all_station_availability.json", "r") as fp:
        all_station_availability = json.load(fp)
    
    return all_station_availability


def get_station_availability(all_station_availability, stationUID, rent):
    """
    Functions that return station's available rent bikes if you'll rent there, 
    if you don't, it will return station's available return bikes

    Parameters:
        all_station_availability: a list store station availability (list)
        stationUID: a unique ID for every Ubike station(provided from PTX) (str)
        rent: If you'll rent bike there (bool)

    Return:
        return a interger
    """
    for station in all_station_availability:
        if station["StationUID"] == stationUID:
            if rent:
                return int(station["AvailableRentBikes"])
            else:
                return int(station["AvailableReturnBikes"])



def search(all_station_availability, all_station_info, cord, rent):
    _min = distance((all_station_info[0]["StationPosition"]["PositionLat"], all_station_info[0]["StationPosition"]["PositionLon"]), cord)
    _name = all_station_info[0]["StationName"]["Zh_tw"]
    _UID = all_station_info[0]["StationUID"]
    _cord = (all_station_info[0]["StationPosition"]["PositionLat"], all_station_info[0]["StationPosition"]["PositionLon"])
    _bike = get_station_availability(all_station_availability, _UID, rent)

    for station in all_station_info[1:]:
        if get_station_availability(all_station_availability, station["StationUID"], rent) > 0:
            temp = distance((station["StationPosition"]["PositionLat"], station["StationPosition"]["PositionLon"]), cord)
            if temp < _min:
                _min = temp
                _name = station["StationName"]["Zh_tw"]
                _UID = station["StationUID"]
                _cord = (station["StationPosition"]["PositionLat"], station["StationPosition"]["PositionLon"])
                _bike = get_station_availability(all_station_availability, _UID, rent)



    return {"name": _name, "UID": _UID, "cord": _cord, "bike": _bike,"rent": rent}


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

app_id = config["PTX"]["APP_ID"] # app_id
app_key = config["PTX"]["APP_KEY"] # app_key

all_station_info = []
all_station_availability = []

cities = [
    "Taipei",
    "Taichung",
    "Taoyuan",
    "NewTaipei",
    "ChanghuaCounty",
    "MiaoliCounty",
    "Hsinchu"
]
'''
臺北: 400
新北: 561
桃園: 305
新竹市 & 竹科: 57
苗栗: 30
臺中: 326
彰化: 68
'''

# use this class, you can get correct header of ptx and get data from it
a = Auth(app_id, app_key)


"""
PTX API, dict type:
{
    'StationUID': 'TPE0001', 
    'StationID': '0001', 
    'AuthorityID': 'TPE', 
    'StationName': {'Zh_tw': '捷運市政府站(3號出口)', 'En': 'MRT Taipei City Hall Stataion(Exit 3)-2'}, 
    'StationPosition': {'PositionLat': 25.0408578889, 'PositionLon': 121.567904444}, 
    'StationAddress': {'Zh_tw': '忠孝東路/松仁路(東南側)', 'En': 'The S.W. side of Road Zhongxiao East Road & Road Chung Yan.'}, 
    'BikesCapacity': 180, 
    'SrcUpdateTime': '2019-08-10T19:14:37+08:00', 
    'UpdateTime': '2019-08-10T19:16:30+08:00'
}
"""
