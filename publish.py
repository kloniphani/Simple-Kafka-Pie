#!/usr/bin/python
import sys
import Adafruit_DHT
import time
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

GPIO.add_event_detect(soundSensor, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(soundSensor, callback)  # assign function to GPIO PIN, Run function on change

while True:
    temp = bmp.read_temperature()
    pressure = bmp.read_pressure()
    altitude = bmp.read_altitude()

    print("Temperature: {0:0.1f} C".format(temp))
    print("Pressure:    {0:0.1f} hPa".format(pressure / 100.0))
    print("Altitude:    {0:0.1f}\n".format(altitude))

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
    try:
        producer.send('bde', value=data)
    except Exception as e: print(e)
    
    sleep(5)
    print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))