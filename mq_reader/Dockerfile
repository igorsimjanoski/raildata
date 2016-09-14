FROM python:2.7

RUN pip install pika && pip install pymongo && pip install lxml

COPY . mq_reader

#ENV MQ_HOST=mq MQ_USER=user1 MQ_PASSWORD=pass1 MQ_VHOST=mqserver.qa.us MQ_QUEUE=qa.us.incoming

WORKDIR /mq_reader/bin

CMD ["python", "start_consumer.py"]



