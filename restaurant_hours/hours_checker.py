from datetime import datetime
from restaurant_hours.constants import WEEKDAYS
from restaurant_hours.csv_parser import parse_restaurant_hours

# ================================================================================
# Constants
# ================================================================================

# Expected timestamp format string
# E.g. '2025-5-19-3:14pm'
TIMESTAMP_FMT = '%Y-%-m-%-d-%-I:%M%p'

# ================================================================================
# Hours Check Logic
# ================================================================================

# TODO: doc and implement
def get_open_restaurants(target_timestamp):
    # TODO: error handling for mismatched format
    target_datetime = datetime.strptime(target_timestamp, TIMESTAMP_FMT)
    target_weekday = WEEKDAYS[target_datetime.weekday()]
