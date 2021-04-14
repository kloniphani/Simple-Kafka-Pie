#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import smbus
import RPi.GPIO as GPIO
from pioneer.BMP180 import BMP180


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

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))

# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# enable TLS
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set("arush", "~Arush@01!")

# connect to HiveMQ Cloud on port 8883
client.connect("d01c03054d0643619521997778f15f5a.s1.eu.hivemq.cloud", 8883)

# subscribe to the topics"
topics = ["iot/kodiak/temperature",
    "iot/kodiak/pressure",
    "iot/kodiak/altitude",
    "iot/kodiak/humidity"]

for topic in topics:
    client.subscribe(topic)

client.loop_start()

while True:
    # reading sensor data
    temp = bmp.read_temperature()
    pressure = bmp.read_pressure()
    altitude = bmp.read_altitude()

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    # publishing sensor data
    client.publish(topics[0], "{0}".format(temperature))
    client.publish(topics[1], "{0}".format(pressure / 100))
    client.publish(topics[2], "{0}".format(altitude))
    client.publish(topics[3], "{0}".format(humidity))

    time.sleep(2)

