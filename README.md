from HsiehBing/Stockcrawler_AWS
## Stockcrawler_AWS
1. 執行過程(CICD)：修改上傳至Github後，若成功merge至main後，會透過Actions(v1.yml)自動自做成docer images，並登錄EC2 surver 更新docker container
2. 功能敘述: #為查詢股價(還有TSE，OTC，小台1，小台2)，P台股當日走勢，C當前匯率，F台股個當日買賣超，E盤後法人，K-K線，V虛擬貨幣價格，*為120日內走勢，**為30日內 走勢，美股大小寫都可以，盤後資訊(ETSE、EFB、EFS、EDB、EDS)，更新股號名稱對照UpDate
### 輸出介面 
主要分為文字輸出與圖像輸出，圖像輸出係透過imgur api顯示

### 功能對照

  | function        | 代碼   | python file          | 說明                              |
  | :----:          | :----: | :----:              | :----                             |
  | finainces       | #      | yfinaince.py        | 台股為yahoo爬蟲，美股為yfinance爬蟲 |
  | Vitual_Currency | V      | virtual_currency.py | 使用binance api                   |
  | Currency        | C      | currency.py         | 爬台灣銀行資訊                     |
  | glucose_graph   | *      | imgur.py            | 使用yfinance                      |
  | sTrendTrad      | F      | Trend_Trad.py       | yahoo爬蟲                         |
  | Draw_candle     | K      | candle.py           | 使用yfinance                      |
  | today_price     | P      | running_price.py    | yahoo爬蟲                         |
  | enddistr        | E      | After_hour.py       | 台灣證交所                         |\

UpDate 更新 r_Input.pkl、r_Output.pkl主要是以dictionary形式查詢股名對應股號  update.py
#### 字體選擇 .font 用SimHei

## MVC(Model Views Controllers)
- Model :負責資料存取
  - update.py、r_Input.pkl、r_Output.pkl、.fonts、fonts、SimHei.ttf \
  *ex ./Model/r_input.pkl*

- View:負責顯示資料\
  - static/tmp

- Controllers :負責處理訊息
  - yfinaince.py、virtual_currency.py、currency.py、imgur.py、Trend_Trad.py、candle.py、running_price.py、After_hour.py \
    *ex from Controllers.yfinance import**
## NGINX設定
* 若在docker環境下執行，需要在/etc/nginx/nginx.conf中設定改為
```
daemon off
```
* 其餘設定如下:
```
# /etc/nginx/conf.d/sett.conf
server{
  server_name haha.tw;
  location / {
    proxy_pass http://localhost:8080;
    proxy redirect off;
    proxy_set_header Host $host:8080;
    proxy_set header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For &proxy_add_x_forwarded_for;
 }
}
```
  *此處server_name需更動，可透過no-ip申請短暫DNS或者至gandi購買
* 在由Let's Encrypt取得憑證 \
  相關說明可參考 https://certbot.eff.org/
  
## DOCKER設定
* docker 安裝
```
yum install -y docker
systemctl start docker
```
* docker 相關設定可由dockerfile 中查看
* 需考慮docker images 大小，可嘗試alpine，但本系統是基於python，alpine在python使用時常常有會有問題，因此改用python:3.8-slim
* docker 重要指令
  * 建立docker images (前提是有先建立好dockerfile)
  ```
  docker build -t {ImageName}:{version} .
  ```
  ex. docker build -t test:1 .\
  ***記得有 .***\
  若無輸入版本會設定為latest
  * 查看docker images
  ```
  docker images
  ```
  * 執行docker images
  ```
  docker run -d --name test1 -p 443:443 test:1
  ```
  -d 為背景執行，執行container名稱為test1，image為test:1
  * 查看docker執行中的container
  ```
  docker ps
  ```
  * 若container在背景中執行，需要進入查看相關資訊
  ```
  docker exec -it test1 /bin/bash
  ```
  * 關閉container
  ```
  docker kill test1
  ```
  * 移除container
  ```
  docker rm test1
  ```
* 其他說明：dockerfile中單一images只能執行一行指令，若要執行多行指令可再使其呼叫shell，如start.sh  
## 其他方法運行方法補充
### gunicorn 運作
```
python3 install gunicorn
gunicorn -D -w 1 --access-logfile gunicorn_access.log --error-logfile gunicorn_error.log -b localhost:8080 app:app
```
* -D為背景運作
* -w為cpu使用數
* -access-logfile 與 --error-logfile 為紀錄用
* -b 指定port

### virtul enviorment 運作
1.建立模組資料夾
```python3
python3 -m venv tutorial-env
```
2.啟動虛擬環境
```
source ~/envs/tutorial-env/bin/activate
```
停用環境
```
deactivate
```
3.在虛擬環境中安裝需要套件
```python3
python3 -m pip install
```
也可以直接由requirements.txt安裝
```python3
python -m pip install -r requirements.txt
```
### systemd 運作
#### 說明:可以透過systemctl start 直接啟動或停止系統
```
sudo su -
#至資料結建立名為app1的systemd 檔案
cd /etc/systemd/system
vim app1.service
```
預設檔案位置為/home/ec2-user/bingbingbot/stockcrawler \
虛擬環境在 /home/ec2-user/bingbingbot/tutorial-env
```
#app1.service
[Unit]
Description = App1 Server
[Service]
WrokingDirectory = /home/ec2-user/bingbingbot/stockcrawler
ExecStart = /home/ec2-user/bingbingbot/tutorial-env/gunicorn \
--workers 1\
--access-logfile /home/ec2-user/bingbingbot/stockcrawler/access.log\
--error-logfile /home/ec2-user/bingbingbot/stockcrawler/error.log\
--capture-output\
--bind localhost:8080 app:app

ExecReload=/bin/kill -s HUP $MAINPID
Restart = on-faile
ExecStop /bin/kill TERM $MAINPID
PrivateTmp = true

Restart = alway
[Install]
WantBy =multi-user.target
```
## 更新日誌
* 2023/2/3 update Trend_trad.py 
* 2023/2/7 update yfinance.py
* 2023/2/8 add character lower
* 2023/2/9 yfinance add up_down_sign
* 2023/2/9 change DNS server
* 2023/2/9 新增README.md
* 2023/2/10 add weather report
* 2023/2/10 add push message
