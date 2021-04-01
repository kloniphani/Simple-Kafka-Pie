#!/usr/bin/python
import sys
import Adafruit_DHT
import time

from confluent_kafka import Producer

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        pass

p = Producer({'bootstrap.servers': '192.168.74.140 :9092'})

try:
    for val in xrange(1, 1000):
        p.produce('mytopic', 'myvalue #{0}'
                  .format(val), callback=acked)
        p.poll(0.5)

except KeyboardInterrupt:
    pass

p.flush(30)

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print("Temp: {0:0.1f} C  Humidity: {1:0.1f} %".format(temperature, humidity))
    
    try:
        p.produce("bde", "{0}".format(temperature), callback=acked)
        p.poll(0.5)

    except KeyboardInterrupt:
        pass

    p.flush(30)