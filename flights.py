import sqlite3
from db import db_path

# adding a new flight
def add_flight(flight_number, departure, arrival, date, time, price, seats=60):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        
        # insert flight information
        c.execute(
            """
            INSERT INTO flights(flight_number, departure, arrival, date, time, price, seats)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """, (flight_number, departure, arrival, date, time, price, seats))
        conn.commit()
        return c.lastrowid

# cancel a flight
def cancel_flight(flight_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
        conn.commit()
        conn.close()
        print(f"Flight with ID {flight_id} canceled successfully!")

# retrieving a specific flight
def search_flight_by_id(flight_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
        return c.fetchone()
    
# searching flights
def search_flights(departure=None, arrival=None, date=None):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        query = "SELECT * FROM flights WHERE 1=1" # add conditions later
        condition = []
        
        # conditions
        if departure:
            query += " AND departure LIKE ?"
            condition.append(f"%{departure}%")
        if arrival:
            query += " AND arrival LIKE ?"
            condition.append(f"%{arrival}%")
        if date:
            query += " AND date = ?"
            condition.append(date)
            
        c.execute(query, condition)
        return c.fetchall()
    
# retrieving all flights  
def get_all_flights():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flights ORDER BY date, time")
        # ("SELECT flight_id, flight_number, departure, arrival, date, time, price FROM flights ORDER BY date, time")
        return c.fetchall()