from pydantic import BaseModel
from enum import Enum

class Airline(Enum):
    DELTA = "Delta"
    SOUTHWEST = "Southwest"
    ALASKA = "Alaska"

class Flights(BaseModel):
    airline_name: str
    flight_num: str
    capacity: int
    estimated_flight_duration: int