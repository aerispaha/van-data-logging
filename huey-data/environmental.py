#!/usr/bin/python

import Adafruit_DHT

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensors = dict(
        A = (Adafruit_DHT.AM2302, 17),
        B = (Adafruit_DHT.DHT22, 4),
    )

while True:
    for sensor_id, sensor_config in sensors.items():
        sensor, pin = sensor_config
        
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        temp_F = temperature*1.8 + 32
        if humidity is not None and temperature is not None:
            print('Temp={0:0.2f}*C ({1:0.02f}*F)  Humidity={2:0.2f}% {3}'.format(temperature, temp_F,  humidity, sensor_id))
        else:
            print('Failed to get reading. Try again!')
