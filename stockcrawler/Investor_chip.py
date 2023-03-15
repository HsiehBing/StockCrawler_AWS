# I
import requests
from bs4 import BeautifulSoup
import datetime  

def investor_chip(msg):
#外資買賣超
    static_result_dic = {"E":"外資","D":"投信","A":"大盤"}
    buy_by_whom_dic = {"E":1,"D":2,"A":6}

    select_whom= static_result_dic[msg[1]]
    buy_by_whom =buy_by_whom_dic[msg[1]]

    #起始項目 用於對照開始
    start_item = 1
    url = f'https://histock.tw/stock/three.aspx'
    web=requests.get(url)
    soup = BeautifulSoup(web.text, "html.parser")

    #判斷日期 如果不同延後一天
    start_item_check = datetime.date.today().strftime('%m/%d')
    if start_item_check == soup.select("table.gvTB")[0].select("tr")[start_item].select("span")[0].get_text(strip=True):
        start_item = start_item
    else: 
        start_item +=1
    today_result =  float(soup.select("table.gvTB")[0].select("tr")[start_item].select("span")[buy_by_whom].get_text(strip=True))
    #判斷買賣超
    static_result = ""
    continue_or_not = ""
    continue_do = 1
    if today_result >0 :
        static_result =  "買超"
        while float(soup.select("table.gvTB")[0].select("tr")[start_item+continue_do].select("span")[buy_by_whom].get_text(strip=True) )> 0 :
            continue_do += 1
            static_result = "連續買超"
        return (f'{select_whom}{static_result} {continue_do}天')
    else :
        static_result =   "賣超"
        while float(soup.select("table.gvTB")[0].select("tr")[start_item+continue_do].select("span")[buy_by_whom].get_text(strip=True) )< 0 :
            continue_do += 1
            static_result = "連續買超"
        return (f'{select_whom}{static_result} {continue_do}天')











