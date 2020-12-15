from unittest import TestCase
from chalicelib.geo_hash.geo_point import GeoPoint


class TestGeoPoint(TestCase):
    def test_to_geo_json(self):
        geo_point = GeoPoint(49.26952, -123.128086, {
            "text": "blah blah",
            "int": 1234567890,
            "bool": True,
            "float": -12.42
        }, "af639f0f-e2f2-47d7-8a37-fdaa59b80bd0")

        self.assertEquals(geo_point.to_geo_json(), {
              "type": "Feature",
              "id": "af639f0f-e2f2-47d7-8a37-fdaa59b80bd0",
              "geometry": {
                  "type": "Point",
                  "coordinates": [49.26952, -123.128086]},
              "properties": {
                  "text": "blah blah",
                  "int": 1234567890,
                  "bool": True,
                  "float": -12.42
              }
          })
