#!/usr/bin/python
# -*- coding: utf-8 -*-

"""base_model.py: IS 211 Assignment 12."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import sqlite3

class QueryBuilder(object):
    """This is the query builder class used to query a db.

    Attributes:
        conn: Connection to the hw13.db sqlite database
        cursor: The cursor for the self.conn
    """
    def __init__(self, table):
        """ 
        The constructor for the QueryBuilder class.
        """
        self.table = table
        self.columns = []
        self.wheres = []
        self.order = []
        self.joins = []

    def cols(self, col):
        self.columns.append(col)
        return self

    def where(self, where, andor = "and"):
        self.wheres.append({"condition": where, "type": andor})
        return self

    def orderBy(self, order):
        self.order.append(order)
        return self

    def join(self, join):
        self.joins.append(join)
        return self

    def get_query(self):
        cols = ", ".join(self.columns) if len(self.columns) > 0 else "*"
        joins = " ".join(self.joins) if len(self.joins) > 0 else ""

        where = "WHERE" if len(self.wheres) > 0 else ""
        first_where = True
        for i, condition in self.wheres:
            if first_where:
                first_where = False
                where += " {}".format(condition.condition)
            else:
                where += " {} {}".format(condition.type, condition.condition)

        order = "ORDER BY {}".format(", ".join(self.order)) if len(self.order) > 0 else ""

        return "SELECT {} FROM {} {} {} {}".format(cols, self.table, joins, where, order)


class BaseModel(object):
    """This is the base class used to load the hw13.db.

    Attributes:
        conn: Connection to the hw13.db sqlite database
        cursor: The cursor for the self.conn
    """

    def __init__(self):
        """ 
        The constructor for the BaseModel class.

        Loads the connection to the hw13.db sqlite database
        and creates the cursor for the connection.
        """
        self.conn = None
        self.cursor = None
        self.table = None
        self.qb = None

    def __connect(self):
        """Method to connect to the database and get the cursor."""
        self.conn = sqlite3.connect('hw13.db')
        self.cursor = self.conn.cursor()

    def __disconnect(self):
        """Method to disconnect from the database."""
        try:
            self.cursor = None
            self.conn.close()
            self.table = None
            self.qb = None
        except:
            print("Database connection could not be closed or wasn't open.")

    def __init_qb(self):
        if not self.qb:
            self.qb = QueryBuilder(self.table) 

    def select(self, col):
        self.qb = self.qb.cols(col)
        return self.qb

    def where(self, where, andor = "and"):
        self.qb = self.qb.where(where, andor)
        return self.qb

    def orderBy(self, order):
        self.qb = self.qb.orderBy(order)
        return self.qb

    def join(self, join):
        self.qb = self.qb.join(join)
        return self.qb
    
    def get(self):
        