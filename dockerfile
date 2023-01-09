FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y nginx
RUN mkdir -m 744 -p /etc/letsencrypt
RUN mkdir -m 744 -p /etc/letsencrypt/live
RUN mkdir -m 744 -p /etc/letsencrypt/live/bingbot.hungtse.tw
RUN rm /etc/nginx/nginx.conf
COPY test.conf /etc/nginx/conf.d/test.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem
COPY ./bingbot.hungtse.tw/fullchain.pem /etc/letsencrypt/live/bingbot.hungtse.tw/fullchain.pem
COPY ./bingbot.hungtse.tw/privkey.pem /etc/letsencrypt/live/bingbot.hungtse.tw/privkey.pem
COPY ./stockcrawler/.fonts/SimHei.ttf /usr/share/fonts/SimHei.ttf

WORKDIR /app
COPY ./stockcrawler/* /app/
RUN apt-get install -y vim
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install  gunicorn
RUN mkdir -m 744 -p /app/.fonts
COPY ./stockcrawler/.fonts/SimHei.ttf /app/.fonts/SimHei.ttf
EXPOSE 8080
EXPOSE 443
ADD start.sh /
RUN chmod +x /start.sh
CMD ["/bin/bash", "-c","/start.sh" ]
