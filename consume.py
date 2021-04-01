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

sense.clear(purple)

from pykafka import KafkaClient

client = KafkaClient(hosts="192.168.0.161,")
client.topics
topic = client.topics['bde']

consumer = topic.get_simple_consumer()
for message in consumer:
    if message is not None:
        print(message.offset, message.value)