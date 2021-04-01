#!/usr/bin/python
import sys
import Adafruit_DHT
import time

humidity, temperature = Adafruit_DHT.read_retry(11, 4)

with topic.get_sync_producer() as producer:
    while True:
        producer.produce("temperature:" + temperature)