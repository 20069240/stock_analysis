# -*- coding: utf-8 -*-

# to_database.py
__author__ = 'adrian'

# server and database storage
import MySQLdb as mdb
from pandas.io import sql

# obtain a database connection to the MySQL instance
db_host = 'LOCALHOST'
db_user = 'USERNAME'
db_pass = 'PASSWORD'
db_name = 'DATABASE'
con = mdb.connect(db_host, db_user, db_pass, db_name)

df.to_sql(con=con, name='stock_data', if_exists='replace', flavor='mysql')
