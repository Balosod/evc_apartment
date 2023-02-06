from fastapi import APIRouter, Depends,status,Response
from fastapi_jwt_auth import AuthJWT
from beanie.operators import RegEx,And,Or,In
from ..utils import upload_image_helper, upload_video_helper
from ..settings import CONFIG_SETTINGS
from server.models.user import User
from server.models.property import Property,ApplicableDiscount,PropertySchema,PropertyImages,PropertyVideos





router = APIRouter()

@router.post("/create",status_code=201)
async def create_property(data:PropertySchema,response:Response,Authorize: AuthJWT = Depends()) -> dict:
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    
    if user.is_admin:
        house_property_type = "EVC_Apartment"
    else:
        house_property_type = "EVCA_Affiliate"
    try:
        if CONFIG_SETTINGS.USE_SPACES:
            image_obj = await upload_image_helper.upload_image_to_S3_bucket(data.images,PropertyImages)
            video_obj = await upload_video_helper.upload_video_to_S3_bucket(data.videos,PropertyVideos)
        else:
            image_obj = await upload_image_helper.upload_image_to_file_path(data.images,PropertyImages)
            video_obj = await upload_video_helper.upload_video_to_file_path(data.videos,PropertyVideos)
        
        price_list = []
        
        for item in data.discount:
            price_obj =  ApplicableDiscount(
                discount_name = item.discount_name,
                price = item.price
            )
            await price_obj.create()
            price_list.append(price_obj)
        
        
        
        house_property = Property(
            name = data.name,
            description = data.description,
            nearest_area = data.nearest_area,
            category = data.category,
            property_type = house_property_type,
            airport = data.airport,
            discount = price_list,
            food_option = data.food_option,
            services = data.services,
            owner_id=user.id,
            image=image_obj,
            video=video_obj,
        )
            
        await house_property.create()
        
        return {"message":"house_property Successfully uploaded"}
    except:
        response.status_code = 400
        return {"message":"Something went wrong"}
    


@router.get("/all",status_code =200)
async def get_all_property(Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    all_property = await Property.find(Property.status == "Approve" , fetch_links=True).to_list()

    return all_property

@router.get("/all/{category}",status_code =200)
async def get_property_by_category(category:str,Authorize: AuthJWT = Depends()) -> dict:
    
    Authorize.jwt_required()
    
    all_property = await Property.find(And((Property.category == category),(Property.status == "Approve")), fetch_links=True).to_list()

    return all_property
    
    
    

