# TODO: Deploy Twitter bot to AWS EC2 instance using Ansible

# Local deployment
FROM python:3.6-alpine

COPY . .

RUN pip3 install -r requirements.txt && mkdir -p images

CMD [ "python3", "bot.py" ]


# docker build -t prayingemantis/cinephile-bot:1 .
# docker run --name cinebot -d prayingemantis/cinephile-bot:1
# docker container ls
# docker logs -t <CONTAINER_NAME>
# docker stop cinephilebot