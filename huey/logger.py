from influxdb import InfluxDBClient
import time
from environmental import get_temp_humidity
from settings import *
import logging
import socket

logging.basicConfig(
    filename='/home/pi/projects/van-data-logging/huey/huey.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logging.info('connected to internet')
        return True
    except socket.error as ex:
        logging.error('not connected to internet: ', ex)
        return False


# first wait until we're connected to internet
while not internet():
    pass


while True:
    try:
        # open client
        client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

        # gather data
        env_data = get_temp_humidity()
        client.write_points(env_data)
        logging.info('wrote points successfully')
        client.close()
    except BaseException as e:
        logging.error(e)

    time.sleep(LOGGER_TIMESTEP)
