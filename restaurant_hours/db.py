from datetime import datetime
import sqlite3
import click
from flask import current_app, g


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
    # TODO: populate init data


@click.command('init-db')
def init_db_command():
    '''Command to clear existing data and create tables.'''
    init_db()
    click.echo('Initialized database.')


# Have python interpret db timestamp values as datetime objects.
sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)