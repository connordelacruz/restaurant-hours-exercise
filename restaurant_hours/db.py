from datetime import datetime
import sqlite3
import click
from flask import current_app, g
from restaurant_hours.csv_parser import parse_restaurant_hours

# ================================================================================
# Flask Functions
# ================================================================================

def init_app(app):
    '''Register database teardown and CLI commands.'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        # Setup connection
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows that behave like dicts
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource('data/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    '''Command to clear existing data and create tables.'''
    click.echo('Building database from schema...')
    init_db()
    click.echo('Parsing CSV data and populating tables...')
    populate_app_data()
    click.echo('Initialized database.')


# ================================================================================
# Restaurant Hours Data
# ================================================================================

def populate_app_data():
    '''Populate db tables from CSV.'''
    db = get_db()
    # Parse data from CSV
    restaurant_hours_data = parse_restaurant_hours()
    populate_restaurant_table(db, restaurant_hours_data)
    populate_hours_table(db, restaurant_hours_data)


def populate_restaurant_table(db, restaurant_hours_data):
    '''Insert restaurant names into table.'''
    # Wrap each name as a tuple to appease executemany()'s formatting requirements
    restaurant_name_tuples = [(name,) for name in restaurant_hours_data.keys()]
    cursor = db.cursor()
    cursor.executemany(
        'INSERT INTO restaurant (name) VALUES (?)',
        restaurant_name_tuples
    )
    db.commit()


def populate_hours_table(db, restaurant_hours_data):
    '''Insert restaurant hours into table.'''
    cursor = db.cursor()
    # Get restaurant names and their IDs for mapping
    cursor.execute('SELECT name,id FROM restaurant')
    rows = cursor.fetchall()
    # Iterate through restaurants
    for row in rows:
        hours_block_tuples = restaurant_hours_data[row['name']]
        for hours_block_tuple in hours_block_tuples:
            cursor.execute(
                'INSERT INTO hours (restaurant_id, days, opens, closes) VALUES (?, ?, ?, ?)',
                (row['id'],) + hours_block_tuple
            )
    db.commit()


def find_open_restaurants(weekday, time_int):
    '''Returns a list of restaurant names that are open at the specified weekday and time.

    :param weekday: Weekday name (formatted to match constants.WEEKDAYS)
    :param time_int: Int representation of the target time in 24 hour format (e.g. 2359 = 11:59pm).

    :return: A list of restaurant names that are open at the specified weekday and time.
    '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT restaurant.name FROM restaurant JOIN hours ON restaurant.id = hours.restaurant_id '
        'WHERE hours.days LIKE ? AND hours.opens <= ? AND hours.closes >= ?',
        (f'%{weekday}%', time_int, time_int)
    )
    rows = cursor.fetchall()
    return [
        row['name'] for row in rows
    ]

# ================================================================================
# sqlite3 Misc
# ================================================================================

# Have python interpret db timestamp values as datetime objects.
sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)