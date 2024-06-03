""" Have these endpoints: 
GET / -> list[airline_name]
GET /:airline_name -> list[flight_num]
GET /:airline_name/:flight_num -> Flight

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num """

import json
from fastapi import FastAPI, HTTPException
from models import Flights, Airline

app = FastAPI()

with open("airlines.json", "r") as f:
    airline_data = json.load(f)

airline_list = list(airline_data.keys())
flight_list = {k: v for k, v in airline_data.items()}

@app.get("/")
async def get_airlines() -> list[str]:
    return airline_list

@app.get("/{airline_name}")
async def get_flights(airline_name: Airline) -> list[str]:
    if airline_name.value not in flight_list:
        raise HTTPException(status_code=404, detail="Airline not found")
    return [flight["flight_num"] for flight in flight_list[airline_name.value]]

@app.get("/{airline_name}/{flight_num}")
async def get_flight_info(airline_name: Airline, flight_num: str) -> Flights:
    if airline_name.value not in flight_list:
        raise HTTPException(status_code=404, detail="Airline not found")
    for flight in flight_list[airline_name.value]:
        if flight["flight_num"] == flight_num:
            flight["airline_name"] = airline_name.value
            return Flights(**flight)
    raise HTTPException(status_code=404, detail="Flight not found")

@app.post("/{airline_name}")
async def add_flight(airline_name: Airline, flight: Flights):
    if airline_name.value not in flight_list:
        flight_list[airline_name.value] = []
    flight_data = {
        "airline_name": flight.airline_name,
        "flight_num": flight.flight_num,
        "capacity": flight.capacity,
        "estimated_flight_duration": flight.estimated_flight_duration,
    }
    flight_list[airline_name.value].append(flight_data)
    return {"message": "Flight added successfully"}

@app.put("/{airline_name}/{flight_num}")
async def update_flight(airline_name: Airline, flight_num: str, flight: Flights):
    airline_flights = flight_list.get(airline_name.value)
    if not airline_flights:
        raise HTTPException(status_code=404, detail="Airline not found")

    for index, existing_flight in enumerate(airline_flights):
        if existing_flight["flight_num"] == flight_num:
            updated_flight = {
                "flight_num": flight.flight_num,
                "capacity": flight.capacity,
                "estimated_flight_duration": flight.estimated_flight_duration,
            }
            airline_flights[index] = updated_flight
            return {"message": "Flight updated successfully"}

    raise HTTPException(status_code=404, detail="Flight not found")

@app.delete("/{airline_name}/{flight_num}")
async def delete_flight(airline_name: Airline, flight_num: str):
    if airline_name.value not in flight_list:
        raise HTTPException(status_code=404, detail="Airline not found")
    for idx, existing_flight in enumerate(flight_list[airline_name.value]):
        if existing_flight["flight_num"] == flight_num:
            del flight_list[airline_name.value][idx]
            return {"message": "Flight deleted successfully"}
    raise HTTPException(status_code=404, detail="Flight not found")
