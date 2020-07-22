FROM python:3.6-alpine

COPY . .

RUN pip3 install -r requirements.txt && mkdir -p cinephilebot/images

WORKDIR /cinephilebot

CMD [ "python3", "bot.py" ]