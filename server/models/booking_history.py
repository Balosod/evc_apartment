from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel


class Booking(Document):
    check_in_date: str
    check_out_date: str
    check_in_number: Optional[int] = 0
    check_out_number: Optional[int] = 0
    apply_discount: int
    owner_id: PydanticObjectId
    property_id: PydanticObjectId

    class Settings:
        name = "bookings"


class BookingSchema(BaseModel):
    check_in_date: str
    check_out_date: str
    apply_discount: int
