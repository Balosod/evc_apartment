from beanie import init_beanie
import motor.motor_asyncio

from server.models.user import User
from server.models.property import (
    Property,
    ApplicableDiscount,
    PropertyImages,
    PropertyVideos,
)
from server.models.booking_history import Booking
from server.models.statistic import TotalStatistic
from server.models.statistic import EachStatistic
from server.models.transaction import Transaction


from .settings import CONFIG_SETTINGS


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG_SETTINGS.DATABASE_URL)
    db_name = client[CONFIG_SETTINGS.DATABASE_NAME]

    await init_beanie(
        database=db_name,
        document_models=[
            User,
            Property,
            ApplicableDiscount,
            PropertyImages,
            Booking,
            TotalStatistic,
            EachStatistic,
            PropertyVideos,
            Transaction,
        ],
    )
