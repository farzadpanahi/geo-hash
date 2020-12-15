# geo-hash
A test RESTFul API to store "pins" with coordinates and custom properties. 

## Tech Stack
This API is built using [AWS Chalice](https://aws.github.io/chalice/) framework. It is using [dynamodb-geo](https://github.com/Sigm0oid/dynamodb-geo.py) python library to read/write geo data points to AWS Dynamodb. 

## Architecture
Python code is deployed on AWS Lambda wihich is invoked by AWS Gateway API. AWS Lambda reads and writes to AWS Dynamodb.

## Data Format
API response is in [GeoJson](https://geojson.org/) Feature Point format.

## How to Use
API Endpoint: https://geo-hash.farzadpanahi.com

API Documentation: [Swagger HUB](https://app.swaggerhub.com/apis/farzadpanahi/rest/1.0)

### Curl Examples
#### Get All Pins
```
$ curl https://geo-hash.farzadpanahi.com/pins
```
Response:
```
[{
    "type": "Feature",
    "id": "3019dc27-55c4-4989-bb99-23ae0431d674",
    "geometry": {
        "type": "Point",
        "coordinates": [49.888379, -119.49777]
    },
    "properties": {
        "city": "kelowna",
        "country": "canada",
        "name": "moo-lix"
    }
}, {
    "type": "Feature",
    "id": "fdf4b86d-88bf-4b10-9670-cc67a0415128",
    "geometry": {
        "type": "Point",
        "coordinates": [49.27985, -123.08105]
    },
    "properties": {
        "city": "vancouver",
        "country": "canada",
        "name": "la casa gelato"
    }
}]
```
#### Get One Pin
```
$ curl https://geo-hash.farzadpanahi.com/pin/49.888379/-119.49777/3019dc27-55c4-4989-bb99-23ae0431d674
```
Response:
```
{
    "type": "Feature",
    "id": "3019dc27-55c4-4989-bb99-23ae0431d674",
    "geometry": {
        "type": "Point",
        "coordinates": [49.888379, -119.49777]
    },
    "properties": {
        "city": "kelowna",
        "country": "canada",
        "name": "moo-lix"
    }
}
```
#### Post One Pin
```
$ curl -H "Content-Type: application/json" -d '{"latitude": 49.27897090851482, "longitude":-123.24946995820568, "properties": {"name": "pink ice-cream", "phone-number": 1778666111, "ice-cream-satisfaction-rate": 1.2, "open-during-covid": true}}' https://geo-hash.farzadpanahi.com/pin
```
Response:
```
{
    "type": "Feature",
    "id": "525fd987-24cd-4993-8890-ea8054f8ba93",
    "geometry": {
        "type": "Point",
        "coordinates": [49.278971, -123.24947]
    },
    "properties": {
        "name": "pink ice-cream",
        "phone-number": 1778666111,
        "ice-cream-satisfaction-rate": 1.2,
        "open-during-covid": true
    }
}
```
#### Query Pins by Radius
```
$ curl https://geo-hash.farzadpanahi.com/pins/cp/49.2695199/-123.12808620000001/rad/50000
```
#### Query Pins by Rectangle
```
$ curl https://geo-hash.farzadpanahi.com/pins/rec/49.321060/-123.311955/49.156079/-122.757145
```

