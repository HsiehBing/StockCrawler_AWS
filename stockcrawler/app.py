from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from yfinaince import *
from imgur import *
from running_price import *
from linebot.models import *
from Trend_Trad import *
from virtual_currency import *
from After_hour import *
from test import *
from candle import *
from currency import *
from update import *
from GetUserId import *
from weather import *
from glo_weather import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import yfinance as yf
import matplotlib as plt
import pyimgur
import pickle
import bs4
import re
import mplfinance
import json
import fear_and_greed

#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('T5Zqw8jYWPqLTdpT46lz06Wbqm3RpDw3mrylWdKdV5YRUXqXw/I4BW1Mmp/M0VgK3kA5r4v/V9r4cH2/gH2PIM46uLoHraHb2DxW8EB8lrPT2GzH1YLgETJ8MDuomMwbeDhk/2T4CUM9RxXC3K1E3AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('fb51bfd54e6dca9668655d34b92ebb71')
MyID = "Ue451eae9392cbbed6c8cda5c47771f8f"
JOJO = "Cf30bbe4bff5f3f1002aae698438b8699"
YLinG ="C420c6fbc0d89e0bdc10f333f504458cf"


#監聽所有來自 /callback 的 Post Request
#######
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, "Invalid signature. Please check your channel access token/channel secret.")
    return 'OK'
#########

@app.route("/")
def hello():
    return "Hello Flask!"
########

@app.route("/PmWd_YLin")
def pushmessage_wd_YLin():
    fear_and_greed = round(float(str(fear_and_greed.get())[21:25]))
    reply_message_YLinG=f'Good morning \n道瓊指數:{finainces("#%5EDJI")[19:]} \n費半指數:{finainces("#%5ESOX")[20:]} \n Fear & Greed Index:{source}'
    line_bot_api.push_message(YLinG,TextSendMessage(reply_message_YLinG))
    return "Send weekday morning message to YLinG success"

@app.route("/PmAh")
def pushmessage_wd_Ah():
    img_url = enddistr("ETSE")
    reply_message = f'{investor_chip("IE")}\n{investor_chip("ID")}\n{investor_chip("IA")}'
    line_bot_api.push_message(YLinG,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    
#    line_bot_api.push_message(YLinG,TextSendMessage(reply_message))
    return "Send after_hour image success"


#########
#處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '#' in msg[0]:
        message =TextSendMessage(finainces(msg)) 
        line_bot_api.reply_message(event.reply_token, message)
    elif 'V' in msg[0] or 'v' in msg[0]:
        message =TextSendMessage(Vitual_Currency(msg)) 
        line_bot_api.reply_message(event.reply_token, message)
    elif 'C' in msg[0] or 'c' in msg[0]:
        img_url = Currency(msg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))    

    elif '*' in msg[0]:
        img_url = glucose_graph(msg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    elif 'F' in msg[0] or 'f' in msg[0]:
        message =TextSendMessage(sTrendTrad(msg)) 
        line_bot_api.reply_message(event.reply_token, message)  
    elif 'K' in msg[0] or 'k' in msg[0]:
        img_url = Draw_candle(msg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))              
    elif 'P' in msg[0] or 'p' in msg[0]:
        img_url = today_price(msg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    elif 'E' in msg[0] or 'e' in msg[0]:
        img_url = enddistr(msg)
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
    elif 'T' in msg[0] or 't' in msg[0]:
        message =TextSendMessage(GETUserId(event)) 
        line_bot_api.reply_message(event.reply_token, message)
    elif 'W' in msg[0] :
        message =TextSendMessage(get_weather(msg))
        line_bot_api.reply_message(event.reply_token, message)
    elif  'w' in msg[0]:
        message =TextSendMessage(get_global_weather(msg))
        line_bot_api.reply_message(event.reply_token, message)
    elif 'UpDate'in msg:
        message =TextSendMessage(renew_data()) 
        line_bot_api.reply_message(event.reply_token, message)
        
    elif '~' in msg[0]:
        message = TextSendMessage(text="測試#為查詢股價(還有TSE,OTC,小台1,小台2)\nP台股當日走勢,\n C當前匯率 F台股個當日買賣超,\nE盤後法人 K-K線\nV虛擬貨幣價格,\n*為120日內走勢,**為30日內走勢,\n W天氣 \n ETSE EFB EFS EDB EDS\n UpDate")
        line_bot_api.reply_message(event.reply_token, message)#
    elif '^' in msg[0]:
        message = TextSendMessage("123")
        line_bot_api.reply_message(event.reply_token, message)
        print(f'{event}')




@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
#import os
#if __name__ == "__main__":
#    port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)
