from fastapi import APIRouter, Depends, status, Response
from fastapi_jwt_auth import AuthJWT
from beanie import PydanticObjectId
from beanie.operators import RegEx, And, Or, In
from server.models.property import Property
from server.models.user import User
from server.models.booking_history import Booking
from server.models.statistic import EachStatistic
from server.models.transaction import Transaction


router = APIRouter()


@router.get("/dashboard/stat", status_code=200)
async def admin_landing_page_affiliate(Authorize: AuthJWT = Depends()) -> dict:

    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    affiliate = await User.find_one(User.email == current_user)

    data = []
    total_sales = 0
    check_in = 0
    check_out = 0
    statistic_list = []
    cities_list = {}
    booked_property = await Booking.find().to_list()
    for item in booked_property:
        property_obj = await Property.find_one(
            And(
                (Property.owner_id == affiliate.id),
                (Property.id == item.property_id),
                (Property.property_type == "EVCA_Affiliate"),
            )
        )
        if property_obj:
            try:
                cities_list[property_obj.nearest_area] += 1
            except:
                cities_list[property_obj.nearest_area] = 1
            total_sales += item.apply_discount
            check_in += item.check_in_number
            check_out += item.check_out_number

    each_statistic = await EachStatistic.find(
        EachStatistic.owner_id == affiliate.id
    ).to_list()

    # for item in each_statistic:
    #     property_obj = await Property.find_one(And((Property.id == item.property_id),(Property.owner_id == affiliate.id),(Property.property_type == "EVCA_Affiliate")))
    #     if property_obj:
    #         print("yes.....")
    #         statistic_list.append(item)

    sorted_cities = sorted(cities_list.items(), key=lambda x: x[1], reverse=True)[0:3]
    top_cites = dict(sorted_cities)

    data.append(top_cites)
    data.append({"total_sales": total_sales})
    data.append({"total_visitors": 0})
    data.append({"check_in": check_in})
    data.append({"check_out": check_out})
    data.append(each_statistic)

    return data


@router.get("/transaction", status_code=200)
async def all_transaction(Authorize: AuthJWT = Depends()) -> dict:

    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    affiliate = await User.find_one(User.email == current_user)

    all_transaction = await Transaction.find(
        Transaction.owner_id == affiliate.id
    ).to_list()

    return all_transaction


@router.get("/all/property", status_code=200)
async def all_property(response: Response, Authorize: AuthJWT = Depends()) -> dict:

    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    user = await User.find_one(User.email == current_user)

    if user.is_affiliate:
        data = {"count": "", "data": ""}
        all_property = await Property.find(
            Property.owner_id == user.id, fetch_links=True
        ).to_list()

        data["count"] = len(all_property)
        data["data"] = all_property

        return data
    else:
        response.status_code = 401
        return {"message": "not an affiliate"}
