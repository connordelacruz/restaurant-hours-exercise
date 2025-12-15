from flask import Flask
from flask_restful import Api, Resource
from csv_parser import main

app = Flask(__name__)
api = Api(app)

class RestaurantHours(Resource):
    def get(self):
        return main()

api.add_resource(RestaurantHours, '/')

if __name__ == '__main__':
    app.run(port=8000, debug=True)