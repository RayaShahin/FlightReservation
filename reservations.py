import sqlite3
from db import db_path

# make a reservation
def make_reservation(passenger_name, flight_id, seat_number):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        
        # make sure the seat is not taken
        c.execute("SELECT seats FROM flights WHERE flight_id = ?", (flight_id,))
        flight = c.fetchone()
        if not flight:
            conn.close()
            return "Flight not found."
        
        available_seats = flight[0]
        if available_seats <= 0:
            return "No seats available."
        
        # add new reservation
        c.execute("INSERT INTO reservations (passenger_name, flight_id) VALUES (?, ?)",
                  (passenger_name, flight_id))
        
        # reduce available seats
        c.execute("UPDATE flights SET seats = seats - 1 WHERE flight_id = ?", (flight_id,))
        
        conn.commit()
        return "Reservation booked successfully"

# cancel a reservation
def cancel_reservation(reservation_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        
        # check if flight and reservation exist
        c.execute("SELECT flight_id FROM reservations WHERE reservation_id = ?", (reservation_id,))
        res = c.fetchone()
        if not res:
            return "Reservation not found."
        
        flight_id = res[0]
        
        # delete reservation
        c.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id,))
        
        # update/increase number of seats available
        c.execute("UPDATE flights SET seats = seats + 1 WHERE flight_id = ?", (flight_id,))
        
        conn.commit()
        return "Reservation canceled successfully."

# retrieving all reservations  
def get_all_reservation():
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
                  SELECT r.reservation_id, r.passenger_name, f.flight_id, f.departure, f.arrival, f.date, f.time
                  FROM reservations r
                  JOIN flights 
                  ON r.flight_id = f.flight_id
                  ORDER BY f.date, f.time
                  """)
        return c.fetchall()