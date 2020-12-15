# Path hack !!! due to sibling package import troubles
# import sys
# import os
# sys.path.insert(0, os.path.abspath('..'))

from chalice import Chalice
from chalicelib.geo_hash.geo_hash import GeoHash
import configparser

app = Chalice(app_name='rest')

config = configparser.ConfigParser()
config.read('chalicelib/config.ini')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/pins')
def get_pins():
    geo_hash = GeoHash(
        config['dynamodb']['region'],
        config['dynamodb']['table'],
        config['dynamodb']['hash_key_length']
    )

    pins = geo_hash.get_geo_points()
    return [pin.to_dict() for pin in pins]
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
