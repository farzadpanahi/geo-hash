#!/usr/bin/env python
"""
creates the geo-table required in dynamodb
make sure you have your aws credentials under ~/.aws
before executing this script use the following command to export the proper aws profile:
$ export AWS_PROFILE=user1
"""
from dynamodb_helper import create_geo_table
AWS_REGION="us-east-1"
TABLE_NAME="geo-hash"

if __name__ == "__main__":
    create_geo_table(AWS_REGION, TABLE_NAME)