#!/usr/bin/env python3
import csv
import pprint

# ================================================================================
# Main (For Testing)
# ================================================================================

def main():
    '''Function to call when file is executed directly.'''
    restaurant_data = {}
    with open('restaurants.csv') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        for row in reader:
            name = row[0]
            hours_string = row[1]
            # TODO: parse hours_string
            restaurant_data[name] = hours_string
    pprint.pp(restaurant_data)


if __name__ == '__main__':
    main()
