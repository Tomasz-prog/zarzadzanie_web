import sqlite3
from datetime import datetime


class Database():

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS projekty (id INTEGER PRIMARY KEY, "
                         "data date, "
                         "projekt_name varchar(255))")

    def insert_project(self, nazwa):

        self.cur.execute(f"INSERT INTO PROJEKTY (data, projekt_name) values('{datetime.today().strftime('%Y-%m-%d')}', "
                         f"'{nazwa}')")
        self.conn.commit()
