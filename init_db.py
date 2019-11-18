#!/usr/bin/python
# -*- coding: utf-8 -*-

"""init_db.py: IS 211 Assignment 12."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import sys
import sqlite3

class StudentQuizzesDB(object):
    """This class is used to create the hw13.db schema and load the data.

    Attributes:
        conn: Connection to the hw13.db sqlite database
        cursor: The cursor for the self.conn
    """

    def __init__(self):
        """ 
        The constructor for StudentQuizzesDB class.

        Loads the connection to the hw13.db sqlite database
        and creates the cursor for the connection.
        """
        self.conn = sqlite3.connect('hw13.db')
        self.cursor = self.conn.cursor()


    def __del__(self):
        """ 
        The destructor for StudentQuizzesDB class.

        Sets the cursor to None and attempts to close
        the database connection.
        """

        try:
            self.cursor = None
            self.conn.close()
            
            # Print success message
            print("Database closed successfully.")

        except:
            # Print error message
            print("Database could not be closed or wasn't open.")


    def create_schema(self):
        """
        Creates the hw13.db schema
        
        Schema description:
            students: Used to store data about students
            quizzes: Used to store data about quizzes
            student_quiz: A many-to-many table that maps
                        student and quiz scores.
        """
        
        try:
            with open('schema.sql', 'r') as s:
                schema = s.read()

            # Execute the script to (re)create the schema
            self.cursor.executescript(schema)

            # Commit the schema
            self.conn.commit()
            
            # Print success message
            print("Created the hw13.db schema")
        
        except:
            # Print error message
            print("Unable to create the hw13.db schema")


    def load_data(self):
        """Loads data into the hw13.db sqlite database"""
        
        try:
            # Insert rows into the users table
            self.cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)",
                                    (
                                        (1, 'System', 'Admin', 'admin', 'password')
                                    )
                                )

            # Insert rows into the students table
            self.cursor.execute("INSERT INTO students VALUES(?, ?, ?)",
                                    (
                                        (10000001, 'John', 'Smith')
                                    )
                                )
                                
            # Insert rows into the quizzes table
            self.cursor.execute("INSERT INTO quizzes VALUES(?, ?, ?, ?)", 
                                    (
                                        (1, 'Python Basics', 5, '2015-02-05')
                                    )
                                )

            # Insert rows into the student_quiz table
            self.cursor.execute("INSERT INTO student_quiz VALUES(?, ?, ?)", 
                                    (
                                        (10000001, 1, 85)
                                    )
                                )
            
            # Commit the data
            self.conn.commit()
            
            # Print success message
            print("Loaded data into hw13.db")
        
        except:
            # Print error message
            print("Unable to load data into hw13.db")


def main():
    """The method that runs when the program is executed."""

    # Instantiate a StudentQuizzesDB object
    student_quizzes_db = StudentQuizzesDB()
    # Create the schema
    student_quizzes_db.create_schema()
    # Load test data
    student_quizzes_db.load_data()
    
    # Exit the program after the db is initialized
    sys.exit()


if __name__ == '__main__':
    main()
