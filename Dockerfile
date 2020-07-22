FROM python:3.6-alpine

COPY . .

RUN pip3 install -r requirements.txt && mkdir -p images

CMD [ "python3", "bot.py" ]