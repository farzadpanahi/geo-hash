import simplejson as json
from geojson import Feature, Point


class GeoPoint(object):
    def __init__(self, latitude, longitude, properties, point_id=None):
        self.latitude = latitude
        self.longitude = longitude
        self.properties = properties
        self.point_id = point_id

    @staticmethod
    def decode_from_dynamodbgeo(dynamodbgeo_dict):
        latitude_longitude = dynamodbgeo_dict['geoJson'].split(',')
        properties = {k: v for (k, v) in dynamodbgeo_dict.items() if k not in ['geoJson', 'geohash', 'hashKey', 'rangeKey']}
        point_id = dynamodbgeo_dict['rangeKey']

        return GeoPoint(float(latitude_longitude[0]), float(latitude_longitude[1]), properties, point_id)

    def __str__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'point_id': self.point_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'properties': self.properties
        }

    def __eq__(self, other):
        if isinstance(other, GeoPoint):
            return (self.point_id == other.point_id and
                    self.latitude == other.latitude and
                    self.longitude == other.longitude and
                    self.properties == other.properties)

        return False

    def to_geo_json(self):
        return Feature(
            id=self.point_id,
            geometry=Point((self.latitude, self.longitude)),
            properties=self.properties
        )