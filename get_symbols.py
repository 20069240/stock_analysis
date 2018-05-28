# -*- coding: utf-8 -*-

# get_symbols.py

import datetime # date and time
import bs4 # web scraping
import MySQLdb as mdb # MySQL server and database storage
import requests # web queries

def parse_wiki():
    # stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    response = requests.get(
        "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    soup = bs4.BeautifulSoup(response.text, "lxml")
    symbolslist = soup.select('table')[0].select('tr')[1:]

    # obtain symbol info for each row in S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
            (
                tds[0].select('a')[0].text,  # ticker
                'stock', 
                tds[1].select('a')[0].text,  # name
                tds[3].text,  # sector
                'USD', now, now
            )     
        )
    return symbols

def insert_symbols(symbols):
    """Insert the S&P500 symbols into the MySQL database."""
    # connect to the MySQL instance
    db_host = 'hostname'
    db_user = 'username'
    db_pass = 'password'
    db_name = 'database'
    con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)

    # create the insert strings
    column_str = """ticker, instrument, name, sector, 
                 currency, created_date, updated_date"""
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # using the MySQL connection, carry out 
    # an INSERT INTO for every symbol
    with con:
        cur = con.cursor()
        cur.executemany(final_str, symbols)

if __name__ == "__main__":
    symbols = parse_wiki()
    insert_symbols(symbols)
    print("""\n
          %s symbols were successfully added.""" % len(symbols))
