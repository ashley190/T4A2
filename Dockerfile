FROM ubuntu:latest
RUN apt-get update
RUN apt-get install python3.8 python3-pip gunicorn -y
WORKDIR /code
COPY src .
RUN pip3 install -r requirements.txt
ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]
