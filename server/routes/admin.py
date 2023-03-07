from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import RegEx,And,Or,In
from server.models.property import Property
from server.models.booking_history import Booking
from server.models.statistic import TotalStatistic
from server.models.transaction import Transaction
from server.models.user import User,EmailSchema
from datetime import date



router = APIRouter()


@router.get("/start",status_code =200)
async def admin_landing_page() -> dict:
    
    #Authorize.jwt_required()
    
    data = []
    total_sales = 0
    check_in = 0
    check_out = 0
    statistic_list = []
    cities_list = {}
    booked_property = await Booking.find().to_list()
    for item in booked_property:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVC_Apartment")))
        if property_obj:
            try:
                cities_list[property_obj.nearest_area] += 1 
            except:
                cities_list[property_obj.nearest_area] = 1 
            total_sales += item.apply_discount
            check_in += item.check_in_number
            check_out += item.check_out_number
                
    total_statistic = await TotalStatistic.find().to_list()
    
    for item in total_statistic:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVC_Apartment")))
        if property_obj:
            print("yes1")
            statistic_list.append(item)
    
    sorted_cities = sorted(cities_list.items(), key=lambda x:x[1],reverse=True)[0:3]
    top_cites = dict(sorted_cities)
    
    
    data.append(top_cites)    
    data.append({"total_sales":total_sales}) 
    data.append({"total_visitors":0}) 
    data.append({"check_in":check_in}) 
    data.append({"check_out":check_out}) 
    data.append(statistic_list)    
          
    return data

@router.get("/affiliate/sales",status_code =200)
async def total_affiliate_sales() -> dict:
    
    #Authorize.jwt_required()
    
    data = []
    total_sales = 0
    check_in = 0
    check_out = 0
    statistic_list = []
    cities_list = {}
    booked_property = await Booking.find().to_list()
    for item in booked_property:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVCA_Affiliate")))
        if property_obj:
            try:
                cities_list[property_obj.nearest_area] += 1 
            except:
                cities_list[property_obj.nearest_area] = 1 
            total_sales += item.apply_discount
            check_in += item.check_in_number
            check_out += item.check_out_number
                
    total_statistic = await TotalStatistic.find().to_list()
    
    for item in total_statistic:
        property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.property_type == "EVCA_Affiliate")))
        if property_obj:
            print("yes")
            statistic_list.append(item)
    
    sorted_cities = sorted(cities_list.items(), key=lambda x:x[1],reverse=True)[0:3]
    top_cites = dict(sorted_cities)
    
    
    data.append(top_cites)    
    data.append({"total_sales":total_sales}) 
    data.append({"total_visitors":0}) 
    data.append({"check_in":check_in}) 
    data.append({"check_out":check_out}) 
    data.append(statistic_list)    
          
    return data



@router.get("/transaction",status_code =200)
async def all_transaction() -> dict:
    
    #Authorize.jwt_required()
    
    all_transaction = await Transaction.find(Transaction.agent == "EVC_Apartment").to_list()

    return all_transaction



@router.get("/all/approved/property",status_code =200)
async def all_approved_property() -> dict:
    
    #Authorize.jwt_required()
    
    all_property = await Property.find(Property.status == "Approve", fetch_links=True).to_list()

    return all_property

@router.get("/all/unapproved/property",status_code =200)
async def all_approved_property() -> dict:
    
    #Authorize.jwt_required()
    
    all_property = await Property.find(Property.status == "Reject", fetch_links=True).to_list()

    return all_property


@router.get("/all/property",status_code =200)
async def all_property() -> dict:
    
    #Authorize.jwt_required()
    
    all_property = await Property.find(fetch_links=True).to_list()

    return all_property


@router.get("/approve/property/{ID}",status_code =201)
async def approve_a_property(ID:PydanticObjectId,response:Response) -> dict:
    
    #Authorize.jwt_required()
    
    try:
        property_obj = await Property.find_one(Property.id == ID,fetch_links=True)
        property_obj.status = "Approve"
        await property_obj.save()

        return {"message":"successful"}
    except Exception as e:
        response.status_code = 400
        return {"message":f"{e}"}
    
    
    
@router.get("/reject/property/{ID}",status_code =201)
async def reject_a_property(ID:PydanticObjectId,response:Response) -> dict:
    
    #Authorize.jwt_required()
    
    try:
        property_obj = await Property.find_one(Property.id == ID,fetch_links=True)
        property_obj.status = "Reject"
        await property_obj.save()

        return {"message":"successful"}
    
    except Exception as e:
        response.status_code = 400
        return {"message":f"{e}"}
    
    
@router.get("/all/affiliate",status_code =200)
async def get_all_affiliate() -> dict:
    
    #Authorize.jwt_required()
    all_affiliate = []
    affiliate_obj = await User.find(And((User.is_affiliate == True),(User.active == True)), fetch_links=True).to_list()
    
    all_affiliate.append({"total_affiliate":len(affiliate_obj)})
    all_affiliate.extend(affiliate_obj)
    return all_affiliate

@router.get("/all/user",status_code =200)
async def get_all_user() -> dict:
    
    #Authorize.jwt_required()
    all_user = []
    user_obj = await User.find(And((User.is_affiliate == False),(User.active == True)), fetch_links=True).to_list()
    
    all_user.append({"total_user":len(user_obj)})
    all_user.extend(user_obj)
    return all_user


@router.post("/add/affiliate",status_code =201)
async def add_an_affiliate(data:EmailSchema,response:Response) -> dict:
    today = date.today()
    #Authorize.jwt_required()
    
    try:
        user = await User.find_one(User.email == data.email)
        user.is_affiliate = True
        user.created = today.strftime("%B %d, %Y")
        await user.save()

        return {"message":" successful"}
    except Exception as e:
        response.status_code = 400
        return {"message":f"{e}"}