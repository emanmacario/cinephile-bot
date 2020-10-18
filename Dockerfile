FROM python:3.6-alpine

COPY . .

RUN pip3 install -r requirements.txt 

WORKDIR /cinephilebot

RUN mkdir -p images

CMD [ "python3", "bot.py" ]