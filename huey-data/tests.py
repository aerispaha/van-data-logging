from datetime import datetime
import unittest
import pandas as pd
from influxdb import DataFrameClient
from .logger import write_to_db
from .settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, TEST_DB_NAME, DB_PROTOCOL, DB_PORT


class LoggerTestCase(unittest.TestCase):
    def setUp(self):

        # Connect to the influx client
        self.client = DataFrameClient(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, TEST_DB_NAME)

        # create database
        self.client.create_database(TEST_DB_NAME)

    def tearDown(self):
        # drop test database
        self.client.drop_database(TEST_DB_NAME)

    def test_write_data(self):
        df = pd.DataFrame(data=list(range(30)),
                          index=pd.date_range(start='2014-11-16',
                                              periods=30, freq='H'), columns=['0'])
        test_data = dict(
            datetime=datetime(1988, 11, 18, 12, 00),
            value=23.823,
            sensor_id='temp-a',
            sensor_type=1,

        )
        print(f'data to write:\n{df.to_string()}')
        self.client.write_points(df, 'demo', protocol=DB_PROTOCOL)

        df1 = self.client.query(f"select * from demo")
        print(f'queried data:\n{df1["demo"]}')


if __name__ == '__main__':
    unittest.main()
