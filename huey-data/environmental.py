#!/usr/bin/python

import Adafruit_DHT
import datetime

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensors = dict(
    A=(Adafruit_DHT.AM2302, 17),
    B=(Adafruit_DHT.DHT22, 4),
)


def get_temp_humidity():

    """
    json_body = [
        {
            "measurement": "environment",
            "tags": {
                "sensor_id": "A",
                "region": "rear"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "temperature": 32.08,
                "humidity": 43.01,
            }
        }
    ]
    """

    json_body = []
    for sensor_id, sensor_config in sensors.items():
        sensor, pin = sensor_config

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # check if we have readings and store in data dict
        if humidity is not None and temperature is not None:

            data = dict(
                measurement='environment',
                tags=dict(sensor_id=sensor_id),
                time=datetime.datetime.now(tz='UTC'),
                fields=dict(
                    temperature=temperature,
                    humidity=humidity,
                )
            )
            json_body.append(data)
            print('Temp={0:0.2f}*C Humidity={1:0.2f}% {2}'.format(temperature, humidity, sensor_id))
        else:
            print('Failed to get reading')

    return json_body

