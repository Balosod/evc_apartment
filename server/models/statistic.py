from typing import Optional, List
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel
from enum import Enum


class ProperyType(str, Enum):
    EVC_Apartment = "EVC_Apartment"
    EVCA_Affiliate = "EVCA_Affiliate"


class TotalStatistic(Document):
    date: str
    reach: int
    agent: ProperyType = ProperyType.EVCA_Affiliate
    property_id: PydanticObjectId

    class Settings:
        name = "total_statistics"


class EachStatistic(Document):
    date: str
    reach: int
    owner_id: PydanticObjectId

    class Settings:
        name = "each_statistics"
