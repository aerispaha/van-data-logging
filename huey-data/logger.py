from influxdb import InfluxDBClient
import time
from environmental import get_temp_humidity
from settings import *
import logging
import socket

logging.basicConfig('huey.log')


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False


# first wait until we're connected to internet
while not internet():
    logging.info('not connected to internet')

client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

while True:
    try:
        # gather data
        env_data = get_temp_humidity()
        client.write_points(env_data)
    except BaseException as e:
        logging.error(e)

    time.sleep(LOGGER_TIMESTEP)
