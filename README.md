---
title: "Ubike Bot"
tags: SITCON, bot, telegram
---
# UBikeAnywhereBot


## Usage
1. 給機器人你目前的位置及目的地 (直接打地址或名稱)
2. 機器人會找出離你目前位置最近且有車的Ubike站點(A)
3. 接著也會找出離目的地最近且有空位的Ubike站點(B)
4. 接著利用 Google Map 規劃出一條 **目前位置 -> A -> B -> 目的地** 的路線，並將這條路線的 Google Map 連結傳給使用者
5. 在行程中，會一直檢查站點B是否還有空位，如果沒有，則再次尋找離目的地最近且有空位的Ubike站點，並重新規劃路線

## What We Need

1. Ubike 即時站點資訊 
> 即時站點資訊並沒有整合，而是分成台北區、新北區、桃園區...
- 台北: [https://data.taipei/#/dataset/detail?id=8ef1626a-892a-4218-8344-f7ac46e1aa48](https://data.taipei/#/dataset/detail?id=8ef1626a-892a-4218-8344-f7ac46e1aa48)
- 新北: [http://data.ntpc.gov.tw/od/detail?oid=71CD1490-A2DF-4198-BEF1-318479775E8A](http://data.ntpc.gov.tw/od/detail?oid=71CD1490-A2DF-4198-BEF1-318479775E8A)
- 桃園: [https://data.tycg.gov.tw/opendata/datalist/datasetMeta?oid=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c](https://data.tycg.gov.tw/opendata/datalist/datasetMeta?oid=5ca2bfc7-9ace-4719-88ae-4034b9a5a55c)
- PTX [https://ptx.transportdata.tw/PTX/Service?categoryName=%E8%87%AA%E8%A1%8C%E8%BB%8A](https://ptx.transportdata.tw/PTX/Service?categoryName=%E8%87%AA%E8%A1%8C%E8%BB%8A)
2. Google Map API
^不需要惹

請參考下列格式:
[https://www.google.com/maps/dir/?api=1&origin=海洋大學&destination=臺灣大學&waypoints=臺北動物園|臺北101&travelmode=driving](https://www.google.com/maps/dir/?api=1&origin=海洋大學&destination=臺灣大學&waypoints=臺北動物園|臺北101&travelmode=driving)

- origin: 起點 (可以是座標、地點名稱、Google的placeID)
- destination: 終點 (可以是座標、地點名稱、Google的placeID)
- waypoints: 中途點 (格式與上面相同，中途點間用`|`分隔)
- travelmode: 導航模式 (driving, walking, motorcycling, etc...)

所以上面那段網址點進去後，會出現Google Maps的導航畫面，路線是 **海洋大學 -> 臺北動物園 -> 臺北101 -> 臺灣大學** 而導航模式是開車