#!/usr/bin/python
import sys
import Adafruit_DHT
import time

humidity, temperature = Adafruit_DHT.read_retry(11, 4)
print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))

from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['192.168.0.161:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(1000):
    data = {'temperature' : temperature}
    producer.send('bde', value=data)
    sleep(5)
    print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))