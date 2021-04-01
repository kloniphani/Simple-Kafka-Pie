#!/usr/bin/python
import sys
import Adafruit_DHT
import time

humidity, temperature = Adafruit_DHT.read_retry(11, 4)

from pykafka import KafkaClient

client = KafkaClient(hosts="192.168.0.161,")
client.topics
topic = client.topics['bde']

with topic.get_sync_producer() as producer:
    while True:
        producer.produce("temperature:" + temperature)
        print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))