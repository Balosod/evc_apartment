from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from enum import Enum


class TransactionStatus(str, Enum):
    Booked = "Booked"
    Check_in = "Check_in"
    Check_out = "Check_out"


class Transaction(Document):
    check_in_date: str
    name: str
    transaction_id: str
    price: int
    agent: str
    status: TransactionStatus = TransactionStatus.Booked
    check_out_date: str
    owner_id: PydanticObjectId
    property_id: PydanticObjectId

    class Settings:
        name = "transactions"
