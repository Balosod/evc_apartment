from fastapi import APIRouter, Depends, Response, status
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import RegEx,And,Or,In
from server.models.booking_history import Booking,BookingSchema
from server.models.statistic import TotalStatistic
from server.models.statistic import EachStatistic
from server.models.transaction import Transaction
from server.models.user import User
from server.models.property import Property
from datetime import date




router = APIRouter()





async def get_ID(itemID):
    propertyID = await Property.get(itemID, fetch_links=True)
    if propertyID:
        return {"id":propertyID.id,"name": propertyID.name,"agent":propertyID.property_type,"owner":propertyID.owner_id}
    else:
        return None
    

@router.post("/create/{itemID}", status_code = 200)
async def book_a_property(data:BookingSchema,itemID:PydanticObjectId,response:Response, Authorize: AuthJWT = Depends()) -> dict:
    
    today = date.today()
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    Id = await get_ID(itemID)
    print(Id)

    if Id:
        booking = Booking(
            check_in_date=data.check_in_date,
            check_out_date=data.check_out_date,
            apply_discount=data.apply_discount,
            owner_id=user.id,
            property_id=Id["id"]
            )
        
        await booking.create()
        
        transaction = Transaction(
            check_in_date=data.check_in_date,
            name=Id["name"],
            transaction_id="1234567890",
            price=data.apply_discount,
            agent=Id["agent"],
            status="Booked",
            check_out_date=data.check_out_date,
            owner_id=Id["owner"],
            property_id=Id["id"]
        )
        await transaction.create()
        
        total_statistic_data = await TotalStatistic.find_one(And((TotalStatistic.date == today.strftime("%b-%d-%Y")),(TotalStatistic.agent == Id["agent"]) ))
        if total_statistic_data:
            updated_statistic_data = await TotalStatistic.get(total_statistic_data.id)
            updated_statistic_data.reach += data.apply_discount
            await updated_statistic_data.save()
        else:
            new_statistic_data = TotalStatistic(date = today.strftime("%b-%d-%Y"),
                                           reach= data.apply_discount,
                                           agent=Id["agent"],
                                           property_id=Id["id"]
                                           )
            await new_statistic_data.create()
            
        if Id["agent"] == "EVCA_Affiliate":
            each_statistic_data = await EachStatistic.find_one(And((EachStatistic.date == today.strftime("%b-%d-%Y")),(EachStatistic.owner_id == Id["owner"]) ))
            if each_statistic_data:
                updated_statistic_data = await EachStatistic.get(each_statistic_data.id)
                updated_statistic_data.reach += data.apply_discount
                await updated_statistic_data.save()
            else:
                each_statistic_data = EachStatistic(date = today.strftime("%b-%d-%Y"),
                                            reach= data.apply_discount,
                                            owner_id=Id["owner"],
                                            )
                await each_statistic_data.create()
            
        return {"message":"successful"}
    else:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Property doesn't exit any more"
        )
    


@router.get("/get/all",status_code =200)
async def get_your_booked_property(Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)
    
    bookings = []
    user_booked_property = await Booking.find(Booking.owner_id == user.id).to_list()
    for item in user_booked_property:
        Id = item.property_id
        property_obj = await Property.get(Id, fetch_links=True)
        bookings.append(property_obj)
         
    return bookings 
