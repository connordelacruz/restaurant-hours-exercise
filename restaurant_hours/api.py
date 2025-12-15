from flask import Flask
from flask_restful import Api, Resource
from restaurant_hours.csv_parser import parse_restaurant_hours

app = Flask(__name__)
api = Api(app)

class RestaurantHours(Resource):
    def get(self, timestamp):
        return parse_restaurant_hours()

api.add_resource(RestaurantHours, '/<string:timestamp>')
