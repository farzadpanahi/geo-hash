import boto3
import dynamodbgeo
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


def get_geo_data_manager_config(aws_region, table_name, hash_key_length):

    dynamodb = boto3.client('dynamodb', region_name=aws_region)
    geo_data_manager_config = dynamodbgeo.GeoDataManagerConfiguration(dynamodb, table_name)
    geo_data_manager_config.hashKeyLength = hash_key_length

    return geo_data_manager_config


def get_table(aws_region, table_name):
    dynamodb = boto3.resource('dynamodb', region_name=aws_region)
    return dynamodb.Table(table_name)


def get_geo_data_manager(aws_region, table_name, hash_key_length):
    geo_data_manager_config = get_geo_data_manager_config(aws_region, table_name, hash_key_length)
    return dynamodbgeo.GeoDataManager(geo_data_manager_config)


def create_geo_table(aws_region, table_name, hash_key_length):

    geo_data_manager_config = get_geo_data_manager_config(aws_region, table_name, hash_key_length)
    table_util = dynamodbgeo.GeoTableUtil(geo_data_manager_config)

    create_table_input = table_util.getCreateTableRequest()
    del create_table_input["ProvisionedThroughput"]
    create_table_input["BillingMode"] = "PAY_PER_REQUEST"

    table_util.create_table(create_table_input)


def boto3_serializer(python_dict):
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k, v in python_dict.items()}


def boto3_deserializer(boto3_attribute_value_dict):
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in boto3_attribute_value_dict.items()}

