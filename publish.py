#!/usr/bin/python
import sys
import Adafruit_DHT
import time
from pykafka import KafkaClient

humidity, temperature = Adafruit_DHT.read_retry(11, 4)

with topic.get_sync_producer() as producer:
    while True:
        producer.produce("temperature:" + temperature)
        print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))