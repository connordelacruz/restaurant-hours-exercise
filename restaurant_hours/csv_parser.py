#!/usr/bin/env python3
import csv
from pprint import pprint
import re

# ================================================================================
# Constants
# ================================================================================

# Weekday names
WEEKDAYS = [
    'Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
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
    parsed_days = parse_days_string(days_string)
    parsed_hours = parse_hours_range_string(hours_string)
    # TODO: for testing
    return {
        'days': parsed_days,
        'hours': parsed_hours,
    }
# TODO: parse_hours_range_string()
# TODO: return dict, only include keys for days in this block


def parse_days_string(days_string):
    '''Takes a string representation of days for an hours block and returns a
    list of each weekday this string represents.

    :param days_string: String of weekdays from an hours block that can include
        ranges of days and jumps between days.

    :return: List of weekdays represented by this string.
    '''
    day_blocks = days_string.split(DAY_JUMP_SEP)
    days_open = []
    for day_block_string in day_blocks:
        if DAY_RANGE_SEP in day_block_string:
            # This is a range of days, so we want to get all days between them.
            days_open.extend(parse_day_range_string(day_block_string))
        else:
            # This is a single day.
            days_open.append(day_block_string)
    return days_open


def parse_day_range_string(day_range_string):
    '''Take a string representation of a range of days (e.g. 'Mon-Fri') and
    return a list of each weekday in that range.

    Assumes the start day appears before the end day in WEEKDAYS.

    :param day_range_string: String representation of a day range.

    :return: List of each day within the range.
    '''
    start, end = day_range_string.split(DAY_RANGE_SEP)
    start_index = WEEKDAYS.index(start)
    end_index = WEEKDAYS.index(end)
    # NOTE: Since the assignment states that we can rely on the formatting of
    #       the CSV, we're assuming the days are valid values in WEEKDAYS and
    #       that start_index < end_index, because that's how all the date
    #       ranges in the file are structured.
    return WEEKDAYS[start_index:end_index + 1]



def parse_hours_range_string(hours_string):
    '''TODO: document'''
    opens, closes = hours_string.split(HOUR_RANGE_SEP)
    # TODO: add minutes if not present
    # TODO: debugging
    return {
        'opens': opens,
        'closes': closes,
    }


# ================================================================================
# Main (For Testing)
# ================================================================================

def main():
    '''Function to call when file is executed directly.'''
    parse_csv('restaurants.csv')


if __name__ == '__main__':
    main()
