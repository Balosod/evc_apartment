from fastapi import APIRouter, Depends, status, Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx, And, Or, In
from ..utils import upload_image_helper, upload_video_helper
from ..settings import CONFIG_SETTINGS
from server.models.user import User
from ..utils.filter_helper import filters
from server.models.property import (
    Property,
    ApplicableDiscount,
    PropertySchema,
    PropertyImages,
    PropertyVideos,
)


router = APIRouter()


@router.post("/create", status_code=201)
async def create_property(
    data: PropertySchema, response: Response, Authorize: AuthJWT = Depends()
) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    user = await User.find_one(User.email == current_user)

    if user.is_admin:
        evc_property_type = "EVC_Apartment"
    else:
        evc_property_type = "EVCA_Affiliate"
    try:
        if CONFIG_SETTINGS.USE_SPACES:
            image_obj = await upload_image_helper.upload_image_to_S3_bucket(
                data.images, PropertyImages
            )
            video_obj = await upload_video_helper.upload_video_to_S3_bucket(
                data.videos, PropertyVideos
            )
        else:
            image_obj = await upload_image_helper.upload_image_to_file_path(
                data.images, PropertyImages
            )
            video_obj = await upload_video_helper.upload_video_to_file_path(
                data.videos, PropertyVideos
            )

        price_list = []

        for item in data.discount:
            price_obj = ApplicableDiscount(
                discount_name=item.discount_name, price=item.price
            )
            await price_obj.create()
            price_list.append(price_obj)

        nearest_area = data.nearest_area.lower()
        evc_property = Property(
            name=data.name,
            description=data.description,
            nearest_area=nearest_area,
            category=data.category,
            property_type=evc_property_type,
            airport=data.airport,
            breakfast=data.breakfast,
            lunch=data.lunch,
            dinner=data.dinner,
            wifi=data.wifi,
            maximum_security=data.maximum_security,
            two_showers=data.two_showers,
            luxury_bedroom=data.luxury_bedroom,
            kitchen=data.kitchen,
            price=data.price,
            capacity=data.capacity,
            discount=price_list,
            owner_id=user.id,
            image=image_obj,
            video=video_obj,
        )

        await evc_property.create()

        return {"message": "successful"}
    except Exception as e:
        response.status_code = 400
        return {"message": f"{e}"}


@router.get("/all", status_code=200)
async def get_all_property(location: str = None, capacity: int = None) -> dict:
    if location:
        return await Property.find(Property.nearest_area == location).to_list()
    return await Property.find_all().to_list()


@router.get("/all/{category}", status_code=200)
async def get_property_by_category(category: str) -> dict:
    return await Property.find(
        And((Property.category == category), (Property.approval_status == True)),
        fetch_links=True,
    ).to_list()
