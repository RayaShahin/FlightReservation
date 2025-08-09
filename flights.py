import sqlite3
from db import db_path

def add_flight(flight_number, departure, arrival, date, time, price):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        
        # insert flight information
        c.execute(
            """
            INSERT INTO flights(flight_number, departure, arrival, date, time, price),
            VALUES(?, ?, ?, ?, ?, ?)
            """, (flight_number, departure, arrival, date, time, price))
        conn.commit()
        return c.lastrowid
    
    