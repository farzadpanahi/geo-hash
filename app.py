from chalice import Chalice, NotFoundError, ChaliceViewError, BadRequestError
from chalicelib.geo_hash.geo_hash import GeoHash
import configparser

app = Chalice(app_name='rest')

config = configparser.ConfigParser()
config.read('chalicelib/config.ini')
geo_hash = GeoHash(
    config['dynamodb']['region'],
    config['dynamodb']['table'],
    config['dynamodb']['hash_key_length']
)

@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/pins')
def get_pins():
    pins = geo_hash.get_geo_points()
    if pins is None:
        raise NotFoundError

    return [pin.to_dict() for pin in pins]


@app.route('/pin/{latitude}/{longitude}/{pinid}')
def get_pin(latitude, longitude, pinid):
    if not _validate_get_pin(latitude, longitude, pinid):
        raise BadRequestError

    pin = geo_hash.get_geo_point(float(latitude), float(longitude), pinid)
    if pin is None:
        raise NotFoundError

    return pin.to_dict()


@app.route('/pin', methods=['POST'])
def post_pin():
    data = app.current_request.json_body
    if not _validate_post_pin(data):
        raise BadRequestError

    pin = geo_hash.add_geo_point(data['latitude'], data['longitude'], data['properties'])
    if pin is None:
        raise ChaliceViewError

    return pin.to_dict()


def _validate_post_pin(body):
    if body is None or len(body) == 0:
        return False

    try:
        latitude = float(body['latitude'])
        longitude = float(body['longitude'])
        properties = body['properties']

        if len(properties) == 0:
            return False

    except:
        return False

    return True


def _validate_get_pin(latitude, longitude, pinid):
    try:
        latitude = float(latitude)
        longitude = float(longitude)

        if pinid is None or len(pinid) == 0:
            return False

    except:
        return False

    return True
