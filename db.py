import sqlite3
from pathlib import Path

db_path = "data/flights.db"

def init_db():
    Path("data").mkdir(exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()       
        # create flights table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS flights(
                      flight_id INTEGER PRIMARY KEY AUTOINCREMEMT,
                      flight_number TEXT NOT NULL,
                      departure TEXT NOT NULL,
                      arrival TEXT NOT NULL,
                      date TEXT NOT NULL, 
                      time TEXT NOT NULL,
                      price REAL NOT NULL
                  )
                  """)
        
        # create reservations table
        c.execute("""
                  CREATE TABLE IF NOT EXISTS reservations(
                      reservation_id INTEGER PRIMARY KEY AUTOINCREMEMT,
                      passenger_name TEXT NOT NULL,
                      contact TEXT,
                      flight_id INTEGER NOT NULL,
                      created_at TEXT DEFAULT (datetime('now','localtime')),
                      FOREIGN KEY(flight_id) REFERENCES flights(flight_id) ON DELETE CASCADE -- to ensure if a flight is deleted then all reservations for it are also deleted
                  """)
        conn.commit()
        conn.close()