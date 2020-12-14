
from dynamodb_helper import get_geo_data_manager, boto3_deserializer, boto3_serializer
from uuid import uuid4
import dynamodbgeo
from pprint import pprint
from geo_json import GeoJsonPoint


class GeoHash(object):
    def __init__(self, aws_region, table_name, hash_key_length):
        self.geo_data_manager = get_geo_data_manager(aws_region, table_name, int(hash_key_length))

    def add_geo_point(self, latitude, longitude, properties):
        item = boto3_serializer(properties)
        point_id = str(uuid4())  # Use this to ensure uniqueness of the hash/range pairs.

        point = dynamodbgeo.PutPointInput(
            dynamodbgeo.GeoPoint(latitude, longitude),
            point_id,
            {
                "Item": item,
                "ConditionExpression": "attribute_not_exists(hashKey)"
            }  # anything else to pass through dynamodb putItem
        )

        response = self.geo_data_manager.put_Point(point)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return GeoJsonPoint(latitude, longitude, properties, point_id)

        return None

    def get_geo_point(self, latitude, longitude, point_id):
        response = self.geo_data_manager.get_Point(dynamodbgeo.GetPointInput(
            dynamodbgeo.GeoPoint(latitude, longitude),
            point_id
        ))

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            item = boto3_deserializer(response['Item'])
            return GeoJsonPoint.decode_from_dynamodbgeo(item)

        return None



    def get_points(self, properties_filter=None):
        pass

    def get_points_by_radius(self, min_point, max_point, properties_filter=None):
        pass

    def get_points_by_rectangle(self, center_point, radius_meter, properties_filter=None):
        pass



