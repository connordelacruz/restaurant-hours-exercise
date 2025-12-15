from flask import Flask
from flask_restful import Api, Resource
# TODO: move import to hours_checker.py
from restaurant_hours.csv_parser import parse_restaurant_hours

class RestaurantHours(Resource):
    def get(self, timestamp):
        # TODO: implement
        return parse_restaurant_hours()


def init_app(app):
    '''Initialize API.'''
    api = Api(app)
    api.add_resource(RestaurantHours, '/<string:timestamp>')
