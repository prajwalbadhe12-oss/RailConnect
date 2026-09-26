from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Passenger:
    name: str
    age: int
    gender: str
    seat_preference: str


@dataclass
class Booking:
    booking_id: str
    pnr: str
    train_id: str
    train_name: str
    source: str
    destination: str
    journey_date: str
    travel_class: str
    passengers: List[Passenger]
    total_amount: float
    status: str = "CONFIRMED"

    def to_dict(self):
        data = asdict(self)
        data["passengers"] = [
            asdict(passenger)
            for passenger in self.passengers
        ]
        return data