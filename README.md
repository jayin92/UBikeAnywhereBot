# UbikeAnywhereBot

***目前專案可能還有bugs，有發現bugs請聯絡我，[t.me/jayinnn](t.me/jayinnn)***

## Introduction
UbikeAnywhereBot 是一款於2019 SITCON 夏令營中開發的Ubike路線規劃Telegram Bot，
可以讓使用者快速的找到最近的且可用的Ubike站點，並藉由Google Maps導航至目的地。

## Usage
Bot 首先會詢問使用者的出發地及目的地（支援模糊搜尋），並利用政府所提供的PTX API取的全台Ubike站點名稱、經緯度、已停車輛、空位，再利用經緯度及已停車輛或空位算出與出發地和目的地可用且最近的Ubike站點，在將這四個位置輸入Google Maps的導航，就完成了一次操作。

## Installatoin
clone後, 請先安裝pipenv，並輸入以下指令
```
pip install pipenv
cd UbikeAnywhereBot
pipenv --three install # install requirements
```

接著請設定`config_template.ini`, 修改後，請重新命名為`config.ini`


```
;Telegram Bot 的 Access Token，請跟@BotFather 申請
[TELEGRAM]
ACCESS_TOKEN = 

; PTX API: https://ptx.transportdata.tw/PTX/ 請先申請帳號
[PTX]
APP_ID = 
APP_KEY = 

; Google Maps API
[GOOGLE]
APP_KEY = 

; Google Firebase API （應該與Google Maps API相同）
[FIREBASE]
API_KEY = 
```

設定完成後，請執行
```
pipenv shell
python main.py
```
這樣就安裝完成了～～～

