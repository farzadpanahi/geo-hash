from unittest import TestCase
from geo_hash import GeoHash
import configparser
from geo_json import GeoJsonPoint
from decimal import Decimal


class TestGeoHash(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = configparser.ConfigParser()
        cls.config.read('../config.ini')

    def test_add_geo_point(self):
        geo_hash = GeoHash(
            self.config['dynamodb']['region'],
            self.config['dynamodb']['table'],
            self.config['dynamodb']['hash_key_length']
        )

        geo_json_point = GeoJsonPoint(23.241369, 20.870348, {'country': 'abc', 'city': 'test', 'number': 123, 'yesno': True, 'number-f': Decimal('123.456')})

        geo_json_point_write = geo_hash.add_geo_point(geo_json_point.latitude, geo_json_point.longitude, geo_json_point.properties)
        print(geo_json_point_write)

        self.assertIsNotNone(geo_json_point_write)

        geo_json_point_read= geo_hash.get_geo_point(23.241369, 20.870348, geo_json_point_write.point_id)
        print(geo_json_point_read)

        self.assertEqual(geo_json_point_write, geo_json_point_read)
