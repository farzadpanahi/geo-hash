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

    return [pin.to_geo_json() for pin in pins]


@app.route('/pins/cp/{latitude}/{longitude}/rad/{radius}')
def get_pins_by_radius(latitude, longitude, radius):
    if not _validate_get_pins_by_radius(latitude, longitude, radius):
        raise BadRequestError

    pins = geo_hash.get_geo_points_by_radius(float(latitude), float(longitude), int(radius))
    if pins is None or len(pins) == 0:
        raise NotFoundError

    return [pin.to_geo_json() for pin in pins]


@app.route('/pins/rec/{min_latitude}/{min_longitude}/{max_latitude}/{max_longitude}')
def get_pins_by_rectangle(min_latitude, min_longitude, max_latitude, max_longitude):
    if not _validate_get_pins_by_rectangle(min_latitude, min_longitude, max_latitude, max_longitude):
        raise BadRequestError

    pins = geo_hash.get_geo_points_by_rectangle(float(min_latitude), float(min_longitude), float(max_latitude), float(max_longitude))
    if pins is None or len(pins) == 0:
        raise NotFoundError

    return [pin.to_geo_json() for pin in pins]


@app.route('/pin/{latitude}/{longitude}/{pinid}')
def get_pin(latitude, longitude, pinid):
    if not _validate_get_pin(latitude, longitude, pinid):
        raise BadRequestError

    pin = geo_hash.get_geo_point(float(latitude), float(longitude), pinid)
    if pin is None:
        raise NotFoundError

    return pin.to_geo_json()


@app.route('/pin', methods=['POST'])
def post_pin():
    data = app.current_request.json_body
    if not _validate_post_pin(data):
        raise BadRequestError

    pin = geo_hash.add_geo_point(data['latitude'], data['longitude'],
                                 data['properties'] if 'properties' in data else {})
    if pin is None:
        raise ChaliceViewError

    return pin.to_geo_json()


def _validate_post_pin(body):
    if body is None or len(body) == 0:
        return False

    try:
        latitude = float(body['latitude'])
        longitude = float(body['longitude'])
        # properties = body['properties']

        # if len(properties) == 0:
        #     return False

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


def _validate_get_pins_by_radius(latitude, longitude, radius):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        radius = int(radius)

        if radius < 0:
            return False
    except:
        return False

    return True


def _validate_get_pins_by_rectangle(min_latitude, min_longitude, max_latitude, max_longitude):
    try:
        min_latitude = float(min_latitude)
        min_longitude = float(min_longitude)
        max_latitude = float(max_latitude)
        max_longitude = float(max_longitude)

    except:
        return False

    return True