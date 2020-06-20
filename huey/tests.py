import unittest
from influxdb import InfluxDBClient
from huey.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, TEST_DB_NAME, DB_PROTOCOL, DB_PORT


class LoggerTestCase(unittest.TestCase):
    def setUp(self):

        # Connect to the influx client
        self.client = InfluxDBClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, TEST_DB_NAME)

        # create database
        self.client.create_database(TEST_DB_NAME)

    def tearDown(self):
        # drop test database
        self.client.drop_database(TEST_DB_NAME)
        self.client.close()

    def test_write_data(self):

        json_body = [
            {
                "measurement": "environment",
                "tags": {
                    "sensor_id": "A",
                    "user": 'randy',
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "temperature": 32.08,
                    "humidity": 43.01,
                }
            },
            {
                "measurement": "environment",
                "tags": {
                    "sensor_id": "B",
                    "user": "randy",
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "temperature": 31.08,
                    "humidity": 42.01,
                }
            },
            {
                "measurement": "environment",
                "tags": {
                    "sensor_id": "B"
                },
                "time": "2009-11-10T23:01:00Z",
                "fields": {
                    "temperature": 32.08,
                    "humidity": 40.01,
                }
            }
        ]

        self.client.write_points(json_body)
        rs = self.client.query('select temperature from environment')
        h = rs.get_points(measurement='environment')

        assert list(h)[0]['temperature'] == 32.08


if __name__ == '__main__':
    unittest.main()
