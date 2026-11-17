from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import Trip
from schemas import TripCreate, ChatRequest
from weather_service import get_weather
from memory import save_session, get_session
from langchain_service import generate_advice

app = FastAPI(
    title="Travel Weather Advisory Assistant",
    description="EY Capstone Assessment",
    version="1.0.0"
)


# ----------------------------------
# DATABASE HELPER
# ----------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------
# ROOT
# ----------------------------------

@app.get("/")
def home():
    return {
        "message": "Travel Weather Advisory Assistant Running"
    }


# ----------------------------------
# CREATE TRIP
# ----------------------------------

@app.post("/trips")
def create_trip(trip: TripCreate):

    try:
        start_date = datetime.strptime(
            trip.start_date,
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            trip.end_date,
            "%Y-%m-%d"
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Date format must be YYYY-MM-DD"
        )

    if end_date < start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    db = SessionLocal()

    try:

        new_trip = Trip(
            employee_id=trip.employee_id,
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
            purpose=trip.purpose,
            status="ACTIVE"
        )

        db.add(new_trip)
        db.commit()
        db.refresh(new_trip)

        return {
            "message": "Trip Created Successfully",
            "trip_id": new_trip.id
        }

    finally:
        db.close()


# ----------------------------------
# GET TRIP
# ----------------------------------

@app.get("/trips/{trip_id}")
def get_trip(trip_id: int):

    db = SessionLocal()

    try:

        trip = (
            db.query(Trip)
            .filter(Trip.id == trip_id)
            .first()
        )

        if not trip:
            raise HTTPException(
                status_code=404,
                detail="Trip Not Found"
            )

        return {
            "trip_id": trip.id,
            "employee_id": trip.employee_id,
            "destination": trip.destination,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "purpose": trip.purpose,
            "status": trip.status
        }

    finally:
        db.close()


# ----------------------------------
# GET LATEST TRIP BY EMPLOYEE
# ----------------------------------

@app.get("/employee/{employee_id}/trip")
def get_latest_trip(employee_id: str):

    db = SessionLocal()

    try:

        trip = (
            db.query(Trip)
            .filter(
                Trip.employee_id == employee_id
            )
            .order_by(
                Trip.id.desc()
            )
            .first()
        )

        if not trip:
            raise HTTPException(
                status_code=404,
                detail="No trips found"
            )

        return {
            "trip_id": trip.id,
            "destination": trip.destination,
            "purpose": trip.purpose,
            "start_date": trip.start_date,
            "end_date": trip.end_date
        }

    finally:
        db.close()


# ----------------------------------
# CHAT ENDPOINT
# ----------------------------------

@app.post("/chat")
def chat(chat_request: ChatRequest):

    try:

        question = chat_request.question
        session_id = chat_request.session_id

        # --------------------------
        # Load Session Memory
        # --------------------------

        session_data = get_session(session_id)

        destination = session_data.get("destination")
        trip_id = session_data.get("trip_id")

        db = SessionLocal()

        try:

            # --------------------------
            # If destination already
            # exists in memory
            # --------------------------

            if destination:

                weather_data = get_weather(destination)

                if not weather_data:
                    return {
                        "answer": (
                            "Weather information "
                            "is currently unavailable."
                        )
                    }

                reply = generate_advice(
                    trip_details={
                        "destination": destination
                    },
                    weather_details=weather_data,
                    question=question
                )

                return {
                    "answer": reply
                }

            # --------------------------
            # First Conversation
            # Find latest trip
            # --------------------------

            latest_trip = (
                db.query(Trip)
                .order_by(Trip.id.desc())
                .first()
            )

            if not latest_trip:
                return {
                    "answer":
                    "No trip found in database. "
                    "Please create a trip first."
                }

            destination = latest_trip.destination

            weather_data = get_weather(destination)

            if weather_data is None:

                return {
                    "answer":
                    f"Unable to retrieve weather "
                    f"for {destination}."
                }

            trip_info = {
                "trip_id": latest_trip.id,
                "employee_id": latest_trip.employee_id,
                "destination": latest_trip.destination,
                "purpose": latest_trip.purpose,
                "start_date": latest_trip.start_date,
                "end_date": latest_trip.end_date
            }

            reply = generate_advice(
                trip_details=trip_info,
                weather_details=weather_data,
                question=question
            )

            save_session(
                session_id,
                {
                    "trip_id": latest_trip.id,
                    "destination": destination
                }
            )

            return {
                "answer": reply
            }

        finally:
            db.close()

    except Exception as e:

        return {
            "answer": f"Error: {str(e)}"
        }


# ----------------------------------
# SESSION INFO
# ----------------------------------

@app.get("/session/{session_id}")
def get_session_info(session_id: str):

    session_data = get_session(session_id)

    if not session_data:
        return {
            "message": "Session Empty"
        }

    return session_data


# ----------------------------------
# CLEAR SESSION
# ----------------------------------

@app.delete("/session/{session_id}")
def clear_session(session_id: str):

    save_session(session_id, {})

    return {
        "message": "Session Cleared"
    }