from datetime import datetime
from restaurant_hours.constants import WEEKDAYS

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
    target_datetime = datetime.strptime(target_timestamp, TIMESTAMP_FMT)

# ================================================================================
# Timestamp Parsing
# ================================================================================

# TODO: doc and implement
def get_day_from_timestamp(timestamp):
    pass
