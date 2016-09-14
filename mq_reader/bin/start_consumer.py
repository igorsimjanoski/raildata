#!/usr/bin/env python
import os
import sys
import time
import json
import ast
from pymongo import MongoClient

import json
import lxml
from lxml import objectify

PROJECT_ROOT = os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
pymodules_path=os.path.join(PROJECT_ROOT, 'pymodules')
sys.path.insert(0, pymodules_path)

from consumers import sample_consumer

class objectJSONEncoder(json.JSONEncoder):
    """A specialized JSON encoder that can handle simple lxml objectify types
       >>> from lxml import objectify
       >>> obj = objectify.fromstring("<Book><price>1.50</price><author>W. Shakespeare</author></Book>")
       >>> json.dumps(obj, cls=objectJSONEncoder)
       '{"price": 1.5, "author": "W. Shakespeare"}'
    """

    model = (
        (objectify.IntElement, int),
        (objectify.NumberElement, float),
        (objectify.FloatElement, float),
        (objectify.ObjectifiedDataElement,
            lambda s: unicode(s).strip().encode('utf-8')),
    )

    def default(self,o):
        for o_type, constructor in self.model:
            if isinstance(o, o_type):
                return constructor(o)
        if hasattr(o, '__dict__'):
            #For objects with a __dict__, return the encoding of the __dict__
            return [item.__dict__ for item in o]
        return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    env = os.environ

    mq_host = 'mq' #env['MQ_HOST']
    mq_user = "" #env['MQ_USER']
    mq_psw = "" #env['MQ_PASSWORD']
    mq_vhost = "/" #env['MQ_VHOST']
    mq_queue = "hello" #env['MQ_QUEUE']

    mq_url = "amqp://%s:%s@%s/%s" %(mq_user, mq_psw, mq_host, mq_vhost)
    print ("Connecting to %s" %mq_url)
     
    decode = objectJSONEncoder()

    client = MongoClient('dbstore', 27017)
    db = client.test
    sc = sample_consumer.SampleConsumer(mq_host, mq_queue)
    while True:
        body, priority, queue =  sc.get_message()
        if body:
	    obj = objectify.fromstring(body) 
       	    #msg = json.loads(body)
	    d = decode.encode(obj)
	    ev = ast.literal_eval(d)
	    msg = ev[0]
            #print("Message fetched %s" %msg) 	
	    try:
	        result = db.trains.insert_one(msg)
	        #print("Message inserted with %s" %result)
	    except Exception as e:
		print e
        else:
            time.sleep(1)

    print("Main process exited")


