---
title: "UbikeAnywhereBot"
tags: SITCON, bot, telegram
---

# UbikeAnywhereBot

## Backgrouds
### Ubike 服務區域
1. 臺北: 400
2. 新北: 561
3. 桃園: 305
4. 新竹市 & 竹科: 57
6. 苗栗: 30
7. 臺中: 326
8. 彰化: 68

**YouBike 全臺站點: 1747**


## Usage
1. 給機器人你目前的位置及目的地 ()
2. 機器人會找出離你目前位置最近且有車的Ubike站點(A)
3. 接著也會找出離目的地最近且有空位的Ubike站點(B)
4. 接著利用 Google Map 規劃出一條 **目前位置 -> A -> B -> 目的地** 的路線，並將這條路線的 Google Map 連結傳給使用者
5. 在行程中，會一直檢查站點B是否還有空位，如果沒有，則再次尋找離目的地最近且有空位的Ubike站點，並重新規劃路線

## Usage(cont.)
1. /start
2. 請問要從這裡出發還是從其他位置出發，現在位置出發請傳送位置資訊，其他位置出發請輸入目的地名稱或地址
3. 若輸入為地址或名稱，則利用Google Maps API回傳經緯度，並利用telegram 地圖服務顯示
4. 請輸入目的地名稱或地址
5. 同 3.
6. (bot 回傳Google Maps導航地址)

## 分工
1. api: 2
> [name= jayinnn, Sean]
2. telegram bot(企劃): 2~3
> [name= 靖軒, kj, Hetty]
3. 簡報: 1
> [name= 潘柏均]

## What We Need

1. Ubike 即時站點資訊 
> 即時站點資訊並沒有整合，而是分成台北區、新北區、桃園區...
- 台北: [https://data.taipei/#/dataset/detail?id=8ef1626a-892a-4218-8344-f7ac46e1aa48](https://data.taipei/#/dataset/detail?id=8ef1626a-892a-4218-8344-f7ac46e1aa48)
- 新北: [http://data.ntpc.gov.tw/od/detail?oid=71CD1490-A2DF-4198-BEF1-318479775E8A](http://data.ntpc.gov.tw/od/detail?oid=71CD1490-A2DF-4198-BEF1-318479775E8A)
- 桃園: [https://data.tycg.gov.tw/opendata/datalist/datasetMeta?oid=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c](https://data.tycg.gov.tw/opendata/datalist/datasetMeta?oid=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c)
- PTX [https://ptx.transportdata.tw/PTX/Service?categoryName=%E8%87%AA%E8%A1%8C%E8%BB%8A](https://ptx.transportdata.tw/PTX/Service?categoryName=%E8%87%AA%E8%A1%8C%E8%BB%8A)
2. Google Map API
- 將地點轉成經緯度


請參考下列格式:
[https://www.google.com/maps/dir/?api=1&origin=海洋大學&destination=臺灣大學&waypoints=臺北動物園|臺北101&travelmode=driving](https://www.google.com/maps/dir/?api=1&origin=海洋大學&destination=臺灣大學&waypoints=臺北動物園|臺北101&travelmode=driving)

- origin: 起點 (可以是座標、地點名稱、Google的placeID)
- destination: 終點 (可以是座標、地點名稱、Google的placeID)
- waypoints: 中途點 (格式與上面相同，中途點間用`|`分隔)
- travelmode: 導航模式 (driving, walking, motorcycling, etc...)

所以上面那段網址點進去後，會出現Google Maps的導航畫面，路線是 **海洋大學 -> 臺北動物園 -> 臺北101 -> 臺灣大學** 而導航模式是開車