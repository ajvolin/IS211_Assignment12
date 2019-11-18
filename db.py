#!/usr/bin/python
# -*- coding: utf-8 -*-

"""db.py: IS 211 Assignment 12."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """Method to get and connect to the database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e = None):
    """Method to close the database if it is open."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """Method to initialize the app instance."""
    app.teardown_appcontext(close_db)