# ptx app id:  839bc6f695d1479a83a04c0e7df512a1
# ptx app key: _Lm4jba4HpNdyXUpjNxgdiLmnlY 


from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import requests as req
from pprint import pprint



app_id = "839bc6f695d1479a83a04c0e7df512a1"
app_key = "_Lm4jba4HpNdyXUpjNxgdiLmnlY"
class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


a = Auth(app_id, app_key)

taoyaun =  req.get("https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Taipei/?$format=JSON", headers=a.get_auth_header())

pprint(taoyaun.json())