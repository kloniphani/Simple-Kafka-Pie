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

import paho.mqtt.client as mqtt

# subscribe to the topics"
topics = ["iot/kodiak/temperature",
    "iot/kodiak/pressure",
    "iot/kodiak/altitude",
    "iot/kodiak/humidity"]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect returned result code: " + str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
    sense_light = []

    # temperature
    if( msg.topic == topics[0]):
        if float(msg.payload.decode("utf-8")) >= 25:
            for i in range(16):
                sense_light.append(red)
        elif float(msg.payload.decode("utf-8")) > 10:
            for i in range(16):
                sense_light.append(orange)
        else:
            for i in range(16):
                sense_light.append(yellow)


    # pressure
    if( msg.topic == topics[0]):
        for i in range(16):
            sense_light.append(purple)

    # altitude
    if( msg.topic == topics[0]):
        if float(msg.payload.decode("utf-8")) >= 0:
            for i in range(16):
                sense_light.append(green)
        else:
            for i in range(16):
                sense_light.append(red)

    # humidity
    if( msg.topic == topics[0]):
        if float(msg.payload.decode("utf-8")) >= 75:
            for i in range(16):
                sense_light.append(green)
        elif float(msg.payload.decode("utf-8")) > 50:
            for i in range(16):
                sense_light.append(yellow)
        elif float(msg.payload.decode("utf-8")) > 25:
            for i in range(16):
                sense_light.append(orange)
        else:
            for i in range(16):
                sense_light.append(red)


    sense.set_pixel(sense_light)


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

for topic in topics:
    client.subscribe(topic)

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()