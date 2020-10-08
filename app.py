import os

from flask import Flask, request
from flask_json import FlaskJSON, as_json, json_response

from web.http import RouteRequest
from web.route_service import RouteServiceFactory

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
json = FlaskJSON(app)
route_service_factory = RouteServiceFactory()


@app.route('/')
def hello_world():
    app_name = os.getenv('APP_NAME')
    if app_name:
        return '{}'.format(app_name)
    return 'Multiple Points Route'

def compute_route(route_request: RouteRequest):
    service = route_service_factory.service(route_request)
    return service.compute_route(route_request)

@app.route('/route', methods=['POST'])
@as_json
def compute_route_default():
    route_request = RouteRequest('ors', 'driving-car', request.json['points'])
    return json_response(route=compute_route(route_request).serialize())

@app.route('/route/<mode>', methods=['POST'])
@as_json
def compute_route_mode(mode: str):
    route_request = RouteRequest('ors', mode, request.json['points'])
    return json_response(route=compute_route(route_request).serialize())

@app.route('/route/<mode>/<service>', methods=['POST'])
@as_json
def compute_route_full(mode: str, service: str):
    route_request = RouteRequest(service, mode, request.json['points'])
    return json_response(route=compute_route(route_request).serialize())

if __name__ == '__main__':
    app.run()
