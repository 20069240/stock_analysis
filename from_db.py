# -*-  Python 3.6   -*-
# -*- Spyder Editor -*-
# -*- coding: utf-8 -*-

"""Created by Adrian Aley on Sun Apr 29 15:10:08 2018"""

# data_storage.py
__author__ = 'adrian'

# server and database storage
import MySQLdb as mdb

# obtain a database connection to the MySQL instance
db_host = 'LOCALHOST'
db_user = 'USERNAME'
db_pass = 'PASSWORD'
db_name = 'DATABASE'
con = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
    """obtains a list of the ticker symbols in the database"""
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[1]) for d in data]

symbols = obtain_list_of_db_tickers()