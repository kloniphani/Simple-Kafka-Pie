from sense_hat import SenseHat
import time
import sys

sense = SenseHat()

red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (160, 32, 240)

sense.set_pixel(4, 5, red)

sense.clear(green)

from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'bde',
     bootstrap_servers=['192.168.0.161:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))


for message in consumer:
    message = message.value
    print(message)