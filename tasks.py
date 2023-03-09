from beanie import init_beanie
import motor.motor_asyncio
import asyncio
from huey import SqliteHuey
from huey import crontab
from server.settings import CONFIG_SETTINGS
from server.models.booking_history import Booking
from datetime import date


huey = SqliteHuey(filename="/tmp/demo.db")


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(CONFIG_SETTINGS.DATABASE_URL)
    db_name = client[CONFIG_SETTINGS.DATABASE_NAME]

    await init_beanie(database=db_name, document_models=[Booking])


async def async_function():
    today = date.today()
    await init_db()
    date = today.strftime("%d/%m/%Y")
    booked_property = await Booking.find().to_list()
    for item in booked_property:
        if item.check_in_date == date and item.check_in_number == 0:
            new_check_in = await Booking.get(item.id)
            new_check_in.check_in_number = 1
            await new_check_in.save()
        if item.check_out_date == date and item.check_out_number == 0:
            new_check_out = await Booking.get(item.id)
            new_check_out.check_out_number = 1
            await new_check_out.save()


@huey.periodic_task(crontab(minute="*/1"))
def add():
    asyncio.run(async_function())
