import Adafruit_DHT

from local_settings import *

DB_PORT = 8086

# seconds between measurements
LOGGER_TIMESTEP=20

SENSORS = dict(
    A=(Adafruit_DHT.AM2302, 17),
    B=(Adafruit_DHT.DHT22, 4),
    C=(Adafruit_DHT.DHT11, 22),
)