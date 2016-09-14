import pika
import json
import time
from pika.exceptions import ConnectionClosed, AMQPConnectionError

class SampleConsumer():
    ''' rabbit consumer using blocking connection adapter'''
    
    def __init__(self, host, queue):
        self.host = host
        self._queue = queue
        print("Going to subscribe executor consumer to host=%s, queue=%s" %(host, queue))
        self.get_channel()
                
    def get_channel(self):
        ''' get connection and channel '''
        channel_not_opened = True
        while channel_not_opened:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
                self.channel = self.connection.channel()
	        self.channel.queue_declare(queue='hello')
                channel_not_opened = False
            except ConnectionClosed:
                #this is thrown in case connection was established, but just before channel was instantiated 
                #connection dropped
                print("Executor consumer connection is closed")
            except AMQPConnectionError as e:
                # this is thrown in case there's connectivity problem to rabbit
                print("Executor consumer AMQP connection error")
            except Exception as e:
                print("Can't get channel")
            else:
                print("Channel successfully created")
            finally:
                if channel_not_opened:
                    print("Channel still not opened , will try again in 15 seconds")
                    time.sleep(15)
    
    def get_message(self, nr_attempts=1):
        ''' get message from queue(with 3 re-try attempts)'''
        try:
            if self.connection.is_open and self.channel.is_open:
                method_frame, properties, body, queue = self._get_sample()
                    
                if method_frame:
                    return body, properties.priority, queue
                else:
                    print("No message fetched from queue")
                    return None, None, None
            else:
                print("Can't get message from queue %s in attempt number %d, connection is closed" %(self._queue, nr_attempts))
                self.get_channel()
                nr_attempts+=1
                if nr_attempts <= 3:
                    return self.get_message(nr_attempts)
                else:
                    return None, None, None
        except Exception as e:
            print("Can't get message from queue %s in attempt number %d" %(self._queue, nr_attempts))
            self.get_channel()
            nr_attempts+=1
            if nr_attempts <= 3:
                return self.get_message(nr_attempts)
            else:
                return None, None, None

    
    def _get_sample(self):
        ''' get sample, first try to get from country queue, if is empty fetch from any queue '''
        queue = method_frame = properties = body = None
        try:
            method_frame, properties, body = self.channel.basic_get(self._queue, no_ack=True)
            queue = self._queue
        except ConnectionClosed:
            print("Can't get sample, connection is closed")
            raise
        except Exception as e:
            print("Can't get sample")
            raise
        return method_frame, properties, body, queue
    
    def close(self):
        try:
            if self.connection and self.channel:
                    self.channel.close()
                    self.connection.close()
        except Exception as e:
            print("Can't close sample consumer")
        else:
            print("Connection and channel from consumer closed")
