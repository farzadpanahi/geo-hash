from unittest import TestCase
from chalicelib.geo_hash.geo_hash import GeoHash
import configparser
from chalicelib.geo_hash.geo_point import GeoPoint
from decimal import Decimal


class TestGeoHash(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = configparser.ConfigParser()
        cls.config.read('../../chalicelib/config.ini')

    def test_add_geo_point(self):
        geo_hash = GeoHash(
            self.config['dynamodb']['region'],
            self.config['dynamodb']['table'],
            self.config['dynamodb']['hash_key_length']
        )

        geo_json_point = GeoPoint(23.241369, 20.870348, {'country': 'abc', 'city': 'test', 'number': 123, 'yesno': True, 'number-f': Decimal('123.456')})

        geo_json_point_write = geo_hash.add_geo_point(geo_json_point.latitude, geo_json_point.longitude, geo_json_point.properties)
        print(geo_json_point_write)

        self.assertIsNotNone(geo_json_point_write)

        geo_json_point_read= geo_hash.get_geo_point(23.241369, 20.870348, geo_json_point_write.point_id)
        print(geo_json_point_read)

        self.assertEqual(geo_json_point_write, geo_json_point_read)

    def test_get_geo_points(self):
        geo_hash = GeoHash(
            self.config['dynamodb']['region'],
            self.config['dynamodb']['table'],
            self.config['dynamodb']['hash_key_length']
        )

        result = geo_hash.get_geo_points()
        self.assertIsNotNone(result)

        for r in result:
            print(r)

        self.assertTrue(len(result) > 0)

    def test_get_geo_points_by_radius(self):
        geo_hash = GeoHash(
            self.config['dynamodb']['region'],
            self.config['dynamodb']['table'],
            self.config['dynamodb']['hash_key_length']
        )

        geo_hash.add_geo_point(49.2695199, -123.12808620000001, {'country': 'canada', 'city': 'vancouver', 'name': 'home'})
        geo_hash.add_geo_point(49.27985, -123.08105, {'country': 'canada', 'city': 'vancouver', 'name': 'la casa gelato'})
        geo_hash.add_geo_point(49.25891, -123.16817, {'country': 'canada', 'city': 'vancouver', 'name': 'la glace'})
        geo_hash.add_geo_point(49.888378706954256, -119.4977704729105, {'country': 'canada', 'city': 'kelowna', 'name': 'moo-lix'})

        result = geo_hash.get_geo_points_by_radius(49.2695199, -123.12808620000001, 50000)  # 50km radius
        # print(result)
        self.assertIsNotNone(result)

        for r in result:
            print(r)

        self.assertTrue(len(result) > 0)
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'la casa gelato', result))) > 0)  # ~25km
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'la glace', result))) > 0)  # ~3km
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'moo-lix', result))) == 0)  # ~270km

    def test_get_geo_points_by_rectangle(self):
        geo_hash = GeoHash(
            self.config['dynamodb']['region'],
            self.config['dynamodb']['table'],
            self.config['dynamodb']['hash_key_length']
        )

        geo_hash.add_geo_point(49.2695199, -123.12808620000001, {'country': 'canada', 'city': 'vancouver', 'name': 'home'})
        geo_hash.add_geo_point(49.27985, -123.08105, {'country': 'canada', 'city': 'vancouver', 'name': 'la casa gelato'})
        geo_hash.add_geo_point(49.25891, -123.16817, {'country': 'canada', 'city': 'vancouver', 'name': 'la glace'})
        geo_hash.add_geo_point(49.888378706954256, -119.4977704729105, {'country': 'canada', 'city': 'kelowna', 'name': 'moo-lix'})

        result = geo_hash.get_geo_points_by_rectangle(49.321060, -123.311955, 49.156079, -122.757145)  # greater vancouver rectangle
        # print(result)
        self.assertIsNotNone(result)

        for r in result:
            print(r)

        self.assertTrue(len(result) > 0)
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'la casa gelato', result))) > 0)  # ~25km
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'la glace', result))) > 0)  # ~3km
        self.assertTrue(len(list(filter(lambda i: i.properties['name'] == 'moo-lix', result))) == 0)  # ~270km


