import sqlite3
from db import db_path

# adding a new flight
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
        conn.close()
        return c.lastrowid
    
# deleting a flight
def remove_flight(flight_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
        conn.commit()
        conn.close()
        print(f"Flight with ID {flight_id} removed successfully!") 


# retrieving all flights  
def get_all_flights():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flights ORDER BY date, time")
        # ("SELECT flight_id, flight_number, departure, arrival, date, time, price FROM flights ORDER BY date, time")
        rows = c.fetchall()
        conn.close()
        return rows

# retrieving a specific flight
def get_flight_by_id(flight_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None
    
# searching flights
def get_flights(departure, arrival, date):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        query = "SELECT * FROM flights WHERE 1=1" # add conditions later
        condition = []
        
        # conditions
        if departure:
            query += "AND departure LIKE ?"
            condition.append(f"%{departure}%")
        if arrival:
            query += "AND arrival LIKE ?"
            condition.append(f"%{arrival}%")
        if date:
            query += "AND date = ?"
            condition.append(date)
            
        c.execute(query, condition)
        rows = c.fetchall()
        conn.close()
        return rows