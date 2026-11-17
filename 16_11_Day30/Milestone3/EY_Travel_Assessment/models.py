from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String)
    destination = Column(String)

    start_date = Column(String)
    end_date = Column(String)

    purpose = Column(String)

    status = Column(String, default="ACTIVE")