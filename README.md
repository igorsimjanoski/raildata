# raildata
RailData POV

**Install Docker**
```
https://docs.docker.com/engine/installation/linux/ubuntulinux/
```

**Clone repository**
```
git clone https://github.com/igorsimjanoski/raildata.git
```

**CD to raildata**
```
cd raildata
```

**Build mq_reader, mq_publisher and mq image**
```
docker build -t mq_reader -f mq_reader/Dockerfile mq_reader/ 
docker build -t mq_publisher -f mq_publisher/Dockerfile mq_publisher/ 
docker build -t mq -f docker_files/mq/Dockerfile docker_files/mq/
```

**Run containers in following order: mongo, mq, mq_reader, mq_publisher**
```
docker run --name dbstore -d mongo
docker run -d --name mq mq
docker run -it -d --link mq:mq --link dbstore:dbstore --name mq_reader mq_reader
docker run -it -d --link mq:mq --name mq_publisher mq_publisher
```

**Find IP of MQ server and access MQ management console**
```
docker inspect --format '{{ .NetworkSettings.IPAddress }}' mq
#default queue=hello is used
http://<MQ_IP>:15672/#/queues
```



