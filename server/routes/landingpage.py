from fastapi import APIRouter, Depends, status, Response
from fastapi_jwt_auth import AuthJWT

from server.models.property import Property


router = APIRouter()


@router.get("/page", status_code=200)
async def landing_page() -> dict:

    # Authorize.jwt_required()
    data = []
    category_context = {}
    location_context = {}
    all_property = await Property.find_all(fetch_links=True).to_list()
    for propert in all_property:
        if propert.category in category_context:
            category_context[propert.category] = category_context[propert.category] + 1
        else:
            category_context[propert.category] = 1
    data.append(category_context)

    for propert in all_property:
        if propert.nearest_area in location_context:
            location_context[propert.nearest_area] = (
                location_context[propert.nearest_area] + 1
            )
        else:
            location_context[propert.nearest_area] = 1
    data.append(location_context)

    return data
