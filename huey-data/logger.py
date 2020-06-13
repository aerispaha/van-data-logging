from influxdb import InfluxDBClient
import time
from environmental import get_temp_humidity
from settings import *


def write_to_db(table, data):
    pass


client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)

while True:

    # gather data
    env_data = get_temp_humidity()
    client.write_points(env_data)

    time.sleep(LOGGER_TIMESTEP)
