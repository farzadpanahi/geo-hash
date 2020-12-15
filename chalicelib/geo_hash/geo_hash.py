from chalicelib.geo_hash.dynamodb_helper import get_geo_data_manager, boto3_deserializer, boto3_serializer, get_table
from uuid import uuid4
import dynamodbgeo
from chalicelib.geo_hash.geo_json import GeoJsonPoint


class GeoHash(object):
    def __init__(self, aws_region, table_name, hash_key_length):
        self.geo_data_manager = get_geo_data_manager(aws_region, table_name, int(hash_key_length))
        self.table = get_table(aws_region, table_name)

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

        if response != 'Error' and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return GeoJsonPoint(latitude, longitude, properties, point_id)

        return None

    def get_geo_point(self, latitude, longitude, point_id):
        response = self.geo_data_manager.get_Point(dynamodbgeo.GetPointInput(
            dynamodbgeo.GeoPoint(latitude, longitude),
            point_id
        ))

        if response != 'Error' and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            item = boto3_deserializer(response['Item'])
            return GeoJsonPoint.decode_from_dynamodbgeo(item)

        return None

    def get_geo_points(self, properties_filter=None):
        response = self.table.scan()  # NOTE: scan has 1MB limit

        if response != 'Error' and response['ResponseMetadata']['HTTPStatusCode'] == 200:
            items = response['Items']
            return [GeoJsonPoint.decode_from_dynamodbgeo(item) for item in items]

        return None

    def get_geo_points_by_radius(self, center_point_latitude, center_point_longitude, radius_meter, properties_filter=None):
        response = self.geo_data_manager.queryRadius(
            dynamodbgeo.QueryRadiusRequest(
                dynamodbgeo.GeoPoint(center_point_latitude, center_point_longitude),
                radius_meter, {}, sort=True
            ))

        if response is not None:
            return [GeoJsonPoint.decode_from_dynamodbgeo(boto3_deserializer(item)) for item in response]

        return None

    def get_geo_points_by_rectangle(self, min_point_latitude, min_point_longitude, max_point_latitude, max_point_longitude, properties_filter=None):
        response = self.geo_data_manager.queryRectangle(
            dynamodbgeo.QueryRectangleRequest(
                dynamodbgeo.GeoPoint(min_point_latitude, min_point_longitude),
                dynamodbgeo.GeoPoint(max_point_latitude, max_point_longitude),
                {}
            ))

        if response is not None:
            return [GeoJsonPoint.decode_from_dynamodbgeo(boto3_deserializer(item)) for item in response]

        return None


