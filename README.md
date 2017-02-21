# PokemonGo-TSP

## Usage
### Requirement

Linux ( Debian / Ubuntu ):
```
pip install -r requirements.txt
```

Linux ( Fedora / Redhat ):
```
pip install -r requirements.txt
```

Mac OSX:
```
pip install -r requirements.txt
```
### Execute
直接執行`python max.py`, 預設會讀取`data/ncku.csv`

跑出結果後會print optimal reward, x, y, 和json檔案，可以用python -m http.server打開index.html結果如附圖

![image](/sample.jpg")


### Execution Options

目前提供了一些命令列參數供大家在執行時比較彈性，可以依據自己的喜好來設定

`-h, --help 可看命令列參數的幫助解說`

`-d, --data 用來設定數據來源（預設值：ncku）`

`-f, --file 使用自己的數據檔案來作計算`

`-t, --time 用來設定時間（預設值：10）`

`-n, --number 用來設定節點數量（預設值：3）`


*附註：如果`-f`和`-d`一起使用，系統將會忽略`-d`*

### Google Map Visualization
執行完`tsp.py`之後，會根據DB內最短路徑產生路徑檔`path.json`，接著開啟index.html就會看到render到Google Map的結果，如下

交大

![NCTU](http://i.imgur.com/alsiSTZ.gif)

東海

![image](http://imgur.com/SbLBsmD.gif)

PS.
- 參考[Google Map API 申請教學](https://pgm.readthedocs.io/en/develop/basic-install/google-maps.html)替換掉`index.html` 中 `{YOUR API KEY}`
- 執行`python -m SimpleHTTPServer` 或者 `python -m http.server`，用瀏覽器開啟`127.0.0.1:8000`，即可看到結果




目前在地理位置之間是用直線，如果用Google Map API 來計算實際地理距離可能會有一個問題，像是操場這種地方會繞一大圈而不是直接穿越

