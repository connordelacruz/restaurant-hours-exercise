#!/usr/bin/env python3
import csv
import os
import re

from restaurant_hours.constants import WEEKDAYS

# ================================================================================
# Constants
# ================================================================================

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
    return restaurant_data

# ================================================================================
# Hours String Helpers
# ================================================================================

def parse_restaurant_hours_string(hours_string):
    '''Takes a full hours string for a restaurant that may include multiple
    hours "blocks" and returns a list of tuples with days, opens, and closes
    hours. See parse_hours_block_string() for more information on tuple format.

    :param hours_string: String representation of a restaurant's hours.

    :return: List of tuples with days, opens, and closes hours.
    '''
    hours_data = []
    # Parse each chunk of the restaurant hours string
    hours_blocks = hours_string.split(BLOCK_SEP)
    for hours_block_string in hours_blocks:
        parsed = parse_hours_block_string(hours_block_string.strip())
        hours_data.extend(parsed)
    return hours_data


def parse_hours_block_string(hours_block_string):
    '''Takes an hours "block" string (i.e. specifies 1 or more days and a range
    of hours) and parses it into a tuple with the following data at each index:

        - 0: Comma-separated weekdays
        - 1: Time restaurant opens
        - 2: Time restaurant closes

    To handle cases where closing hours are past midnight (i.e. bleed into the
    next day), closing times will cap at 1159, then an additional tuple entry
    will be added for the days/times that bleed over.

    :param hours_block_string: String representation of a hours block.

    :return: List of tuples with days, opens, and closes hours.
    '''
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
    opens, closes = parse_hours_range_string(hours_string)
    parsed_days_string = ','.join(parsed_days)

    to_return = []
    # Handle case where closing hours are past midnight and bleed into the next day.
    if closes < opens:
        original_closes = closes
        # Consider this block ending at 11:59pm
        closes = 2359
        # Generate an entry for the time that bleeds into the next day
        to_return.append(create_after_midnight_hours_block(original_closes, parsed_days))
    # NOTE: ordering shouldn't matter, but putting the midnight bleed block after reads a little better.
    to_return.insert(0, (parsed_days_string, opens, closes))

    return to_return


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


def parse_hours_range_string(hours_range_string):
    '''Returns tuple with open and closing hours converted to ints.

    :param hours_range_string: String representation of a range of hours.

    :return: Tuple with open and closing hours converted to ints.
    '''
    opens, closes = hours_range_string.split(HOUR_RANGE_SEP)
    return (
        sanitize_hours_string(opens),
        sanitize_hours_string(closes),
    )


def sanitize_hours_string(hours_string):
    '''Make sure time strings are formatted consistently, then converts to an
    integer representation for easier comparisons.

    Some hours omit the minutes if it's exactly on the hour. In those cases,
    add ':00' as the minutes.

    :param hours_string: String representation of open/close hours. May or may
        not include minutes.

    :return: Integer representation of the time.
    '''
    expr = r'^(\d{1,2}):?(\d{2})?\s([ap]m)$'
    # NOTE: We're assuming this expression will always match since the exercise states that the CSV data will always be well-formed.
    hours, minutes, period = re.findall(expr, hours_string)[0]
    # If minutes were not specified, append them for consistency.
    if minutes == '':
        minutes = '00'
    return convert_time_to_int(hours, minutes, period)


# TODO: extract for reuse for API parsing
def convert_time_to_int(hours, minutes, period):
    '''Convert 12-hour time string representation to an integer representation
    of the 24 hour time.

    :param hours: String representation of hours.
    :param minutes: String representation of minutes.
    :param period: String representation of period (am/pm).

    :return: Integer representing the 24 hour time.
    '''
    period = period.lower()
    hours_int = int(hours)
    if period == 'pm' and hours_int < 12:
        hours_int = hours_int + 12
    elif period == 'am' and hours_int == 12:
        hours_int = 0
    minutes_int = int(minutes)
    return (hours_int * 100) + minutes_int


def create_after_midnight_hours_block(original_closes, original_days):
    '''Returns an hours block to handle when hours are past midnight and
    technically bleed into the next day.

    For each day in the listed hours, shift to the following day. Set opens
    time to 0 and closes time to the original closing time.

    :param original_closes: Original close time as an int.
    :param original_days: List of days from original listing.

    :return: Tuple with days string followed by open and close times as integers.
    '''
    midnight_bleed_day_indexes = []
    # For each original day, get the next day in the week (where post-midnight hours bleed into)
    for original_day in original_days:
        midnight_bleed_day_index = (WEEKDAYS.index(original_day) + 1) % len(WEEKDAYS)
        midnight_bleed_day_indexes.append(midnight_bleed_day_index)
    # NOTE: Implementation doesn't require sorting the days, but it's nice to have consistent ordering
    midnight_bleed_days = [
        WEEKDAYS[i] for i in sorted(midnight_bleed_day_indexes)
    ]
    midnight_bleed_days_string = ','.join(midnight_bleed_days)
    # Return a block where start time is midnight and end time is the original close time
    return (midnight_bleed_days_string, 0, original_closes)


# ================================================================================
# Main
# ================================================================================

def parse_restaurant_hours():
    '''Function to call when file is executed directly.'''
    package_root_dir = os.path.dirname(__file__)
    # TODO: take filepath as parameter
    data_dir = os.path.join(package_root_dir, 'data')
    csv_path = os.path.join(data_dir, 'restaurants.csv')
    return parse_csv(csv_path)


if __name__ == '__main__':
    parse_restaurant_hours()
