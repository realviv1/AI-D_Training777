from database import SessionLocal
from models import Trip

from weather_service import get_weather

def get_trip(trip_id):

    db = SessionLocal()

    trip = db.query(Trip).filter(
        Trip.id == trip_id
    ).first()

    db.close()

    if not trip:
        return None

    return {
        "trip_id": trip.id,
        "employee_id": trip.employee_id,
        "destination": trip.destination,
        "purpose": trip.purpose
    }

def get_trip_by_destination(city):

    db = SessionLocal()

    trip = db.query(Trip).filter(
        Trip.destination.ilike(city)
    ).first()

    db.close()

    return trip