#!/usr/bin/env python3
import csv
from pprint import pprint
import re

# ================================================================================
# Constants
# ================================================================================

# Weekday names
WEEKDAYS = [
    'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
]

# Hours string separators
BLOCK_SEP = '/'
DAY_RANGE_SEP = '-'
DAY_JUMP_SEP = ', '
HOUR_RANGE_SEP = ' - '

# ================================================================================
# File Parsing
# ================================================================================

def parse_csv(filename):
    '''Process CSV file with the provided filename.'''
    restaurant_data = {}
    with open(filename) as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        for row in reader:
            name = row[0]
            hours_string = row[1]
            restaurant_data[name] = parse_restaurant_hours_string(hours_string)
    # TODO: return something
    pprint(restaurant_data)

# ================================================================================
# Hours String Helpers
# ================================================================================

def parse_restaurant_hours_string(hours_string):
    '''TODO: document'''
    # Initialize return value, default to False (closed) for each day
    hours_data = {day: False for day in WEEKDAYS}
    # TODO: for testing
    debug_hours_data = []
    # Parse each chunk of the restaurant hours string
    hours_blocks = hours_string.split(BLOCK_SEP)
    for hours_block_string in hours_blocks:
        hours_block_string = hours_block_string.strip()
        # TODO: implement for real
        parsed = parse_hours_block_string(hours_block_string)
        debug_hours_data.append(parsed)

    # TODO: for testing
    return debug_hours_data


def parse_hours_block_string(hours_block_string):
    '''TODO: document'''
    # Expression to split the hours block into weekdays and times.
    # Since the first part of an hours block is the days of the week, the first
    # match group simply needs to match non-numeric characters.
    # The second part of an hours block will always start with a numeric
    # character and run to the end of the string.
    # In between both groups is a single space.
    expr = r'^(\D+)\s(\d.*)$'
    # NOTE: Because the rules of the assignment assure that CSV data will be
    #       well-formed and correct, we're assuming we will always have a valid
    #       match. For a real-world project I would implement validation and
    #       error handling, but we'll keep things simple for the scope of the
    #       exercise.
    days_string, hours_string = re.findall(expr, hours_block_string)[0]
    # TODO: for testing
    return {'days': days_string, 'hours': hours_string}
    # TODO: parse_days_string()
    # TODO: parse_hours_range_string()
    # TODO: return dict, only include keys for days in this block


def parse_days_string(days_string):
    '''TODO: document'''
    # TODO: split on DAY_JUMP_SEP
    # TODO: for each day chunk, expand any ranges
    # TODO: after expanding, return array with all days in string
    pass


def parse_hours_range_string(hours_string):
    '''TODO: document'''
    # TODO: split open/close on HOUR_RANGE_SEP
    # TODO: add minutes if not present
    # TODO: return {open: open_time_string, close: close_time_string}
    pass


# ================================================================================
# Main (For Testing)
# ================================================================================

def main():
    '''Function to call when file is executed directly.'''
    parse_csv('restaurants.csv')


if __name__ == '__main__':
    main()
