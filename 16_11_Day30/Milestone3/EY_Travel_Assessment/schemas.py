from pydantic import BaseModel

class TripCreate(BaseModel):
    employee_id:str
    destination:str
    start_date:str
    end_date:str
    purpose:str


class ChatRequest(BaseModel):
    session_id:str
    question:str


class ChatResponse(BaseModel):
    answer:str