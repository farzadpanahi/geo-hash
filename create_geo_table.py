#!/usr/bin/env python

"""
creates the geo-table required in dynamodb
make sure you have your aws credentials under ~/.aws
before executing this script use the following command to export the proper aws profile:
$ export AWS_PROFILE=user1
"""

from chalicelib.geo_hash.dynamodb_helper import create_geo_table
import configparser


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    create_geo_table(
        config['dynamodb']['region'],
        config['dynamodb']['table'],
        config['dynamodb']['hash_key_length']
    )