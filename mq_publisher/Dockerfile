FROM python:2.7

RUN pip install pika

COPY . mq_publisher

#ENV MQ_HOST=mq MQ_USER=user1 MQ_PASSWORD=pass1 MQ_VHOST=mqserver.qa.us MQ_QUEUE=qa.us.incoming

WORKDIR /mq_publisher/bin

RUN chmod 755 start_publisher.py

CMD ["./start_publisher.py"]


