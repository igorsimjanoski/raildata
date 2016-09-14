#!/usr/bin/env python
import pika
import time
import random
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('mq'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.close()

while True:
    try:
        channel = connection.channel()
	#msg = {"id" : random.randint(1, 1000), "name" : "sth"}
	msg = '''
        <WagonPerformanceMessage>
        <MessageHeader>
        <MessageReference>
        <MessageType>5500</MessageType>
        <MessageTypeVersion>WPM0100</MessageTypeVersion>
        <MessageIdentifier>UIP_KM-PRO2016-06-10T03:11:36Z</MessageIdentifier>
        <MessageDateTime>2016-06-10T03:11:36Z</MessageDateTime>
        </MessageReference>
        <SenderReference>UIP_KM-PRO2016-06-10T03:11:36Z</SenderReference>
        <Sender>0016</Sender>
        <Recipient>3241</Recipient>
        </MessageHeader>
        <WagonNumberFreight>338078360926</WagonNumberFreight>
        <OperatingRU>2185</OperatingRU>
        <ReportingPeriodSection>
        <DataRecordID>61703887</DataRecordID>
        <StartDateTime>2016-06-09T14:24:00</StartDateTime>
        <EndDateTime>2016-06-09T14:57:00</EndDateTime>
        <Territory>
        <CountryCodeISO>CH</CountryCodeISO>
        </Territory>
        <LoadingStatus>0</LoadingStatus>
        <WagonMileage>29</WagonMileage>
        <WagonPerformanceData>
        <Weight>2.5</Weight>
        <IncludingTareWeight>true</IncludingTareWeight>
        </WagonPerformanceData>
        </ReportingPeriodSection>
        <ReportingPeriodSection>
        <DataRecordID>61703888</DataRecordID>
        <StartDateTime>2016-06-09T16:52:00</StartDateTime>
        <EndDateTime>2016-06-09T18:00:00</EndDateTime>
        <Territory>
        <CountryCodeISO>CH</CountryCodeISO>
        </Territory>
        <LoadingStatus>0</LoadingStatus>
        <WagonMileage>69</WagonMileage>
        <WagonPerformanceData>
        <Weight>2.5</Weight>
        <IncludingTareWeight>true</IncludingTareWeight>
        </WagonPerformanceData>
        </ReportingPeriodSection>
        <ReportingPeriodSection>
        <DataRecordID>61703889</DataRecordID>
        <StartDateTime>2016-06-09T20:20:00</StartDateTime>
        <EndDateTime>2016-06-09T20:28:00</EndDateTime>
        <Territory>
        <CountryCodeISO>CH</CountryCodeISO>
        </Territory>
        <LoadingStatus>0</LoadingStatus>
        <WagonMileage>6</WagonMileage>
        <WagonPerformanceData>
        <Weight>2.5</Weight>
        <IncludingTareWeight>true</IncludingTareWeight>
        </WagonPerformanceData>
        </ReportingPeriodSection>
        </WagonPerformanceMessage>
	'''
        channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=msg)
        print(" [x] Sent 'Hello World!'")
        #time.sleep(100)
    except Exception as e:
	print e
    finally:
	channel.close()


