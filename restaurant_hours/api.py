from datetime import datetime
from flask_restful import Api, Resource
from restaurant_hours.constants import WEEKDAYS
from restaurant_hours.db import find_open_restaurants

# ================================================================================
# Constants
# ================================================================================

# Expected timestamp format string
# E.g. '2025-5-19-3:14pm'
TIMESTAMP_FMT = '%Y-%-m-%-d-%-I:%M%p'

# ================================================================================
# Resources
# ================================================================================

class RestaurantHours(Resource):
    def get(self, timestamp):
        '''Parses a timestamp in the format specified by TIMESTAMP_FMT and
        returns a list of restaurant names that are open at that day/time.

        :param timestamp: GET parameter for the target day/time in the format
            specified by TIMESTAMP_FMT.

        :return: List of restaurant names that are open at the specified
            day/time. If timestamp could not be parsed, will return an error
            message instead.
        '''
        try:
            target_datetime = datetime.strptime(timestamp, TIMESTAMP_FMT)
        except ValueError as e:
            msg = {
                'error': 'Timestamp must be in format YYYY-M-D-h:mmp (e.g. "2025-5-19-2:30pm")'
            }
            return msg, 400
        target_weekday = WEEKDAYS[target_datetime.weekday()]
        # Converted target time to int representation of 24 hour time.
        target_time_int = (target_datetime.hour * 100) + target_datetime.minute
        return find_open_restaurants(target_weekday, target_time_int)


# ================================================================================
# Register API in Flask App
# ================================================================================

def init_app(app):
    '''Initialize API.'''
    api = Api(app)
    api.add_resource(RestaurantHours, '/<string:timestamp>')
