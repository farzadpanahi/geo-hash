import boto3
import dynamodbgeo
import uuid


def get_geo_data_manager_config(aws_region, table_name):

    dynamodb = boto3.client('dynamodb', region_name=aws_region)
    return dynamodbgeo.GeoDataManagerConfiguration(dynamodb, table_name)


def get_geo_data_manager(aws_region, table_name):
    geo_data_manager_config = get_geo_data_manager_config(aws_region, table_name)
    return dynamodbgeo.GeoDataManager(geo_data_manager_config)


def create_geo_table(aws_region, table_name, hash_key_length=6):

    geo_data_manager_config = get_geo_data_manager_config(aws_region, table_name)
    geo_data_manager_config.hashKeyLength = hash_key_length
    table_util = dynamodbgeo.GeoTableUtil(geo_data_manager_config)

    create_table_input = table_util.getCreateTableRequest()
    del create_table_input["ProvisionedThroughput"]
    create_table_input["BillingMode"] = "PAY_PER_REQUEST"

    table_util.create_table(create_table_input)