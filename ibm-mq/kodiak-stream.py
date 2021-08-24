#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import smbus
import RPi.GPIO as GPIO
from pioneer.BMP180 import BMP180
import pymqi
import json


bmp = BMP180()

#GPIO SETUP
soundSensor = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(soundSensor, GPIO.IN)

def callback(soundSensor):
        if GPIO.input(soundSensor):
                print("Sound Detected!")
        else:
                print("Sound Detected!")

#GPIO.add_event_detect(soundSensor, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
#GPIO.add_event_callback(soundSensor, callback)  # assign function to GPIO PIN, Run function on change

# subscribe to the topics"
topics = ["iot/kodiak/temperature",
    "iot/kodiak/pressure",
    "iot/kodiak/altitude",
    "iot/kodiak/humidity"]

# create the client
with open('ibm-mq-ccdt.json', 'r') as connection_file:
    connection = json.load(connection_file)

    queue_manager = connection['channel'][0]['queueManager']
    channel = connection['channel'][0]['name']
    host = connection['channel'][0]['clientConnection']['connection'][0]['host']
    port = connection['channel'][0]['clientConnection']['connection'][0]['port']
    queue_name = 'DEV.QUEUE.1'

    conn_info = '%s(%s)' % (host, port)

    qmgr = pymqi.QueueManager(None)
    qmgr.connect_tcp_client(queue_manager, pymqi.CD(), channel, conn_info)

    while True:
        # reading sensor data
        temp = bmp.read_temperature()
        pressure = bmp.read_pressure()
        altitude = bmp.read_altitude()

        humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        # publishing sensor data
        topic = pymqi.Topic(qmgr, topic_string=topics[0])
        topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
        topic.pub("{0}".format(temperature))
        topic.close()

        topic = pymqi.Topic(qmgr, topic_string=topics[1])
        topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
        topic.pub("{0}".format(pressure / 100))
        topic.close()

        topic = pymqi.Topic(qmgr, topic_string=topics[2])
        topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
        topic.pub("{0}".format(altitude))
        topic.close()

        topic = pymqi.Topic(qmgr, topic_string=topics[3])
        topic.open(open_opts=pymqi.CMQC.MQOO_OUTPUT)
        topic.pub("{0}".format(humidity))
        topic.close()

        time.sleep(20)

    qmgr.disconnect()