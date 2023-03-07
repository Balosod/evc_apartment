from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from beanie import Document, Link,PydanticObjectId
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum


class ProperyType(str,Enum):
    EVC_Apartment = "EVC_Apartment"
    EVCA_Affiliate = "EVCA_Affiliate"
    

    
class PropertyCategory(str,Enum):
    Apartment = "Apartment"
    Room = "Room"
    Short_Stay = "Short_Stay"
    Experience = "Experience"
    Bed_And_Breakfast = "Bed_&_Breakfast"
    
class ApplicableDiscount(Document):
    discount_name:str
    price:int
    
    class Settings:
        name = "applicable discounts"
        
     
class PropertyImages(Document):
    img:str
    
    class Settings:
        name = "property_image"
        
        
class PropertyVideos(Document):
    img:str
    
    class Settings:
        name = "property_video"
    
       
class Property(Document):
    name:str
    description:str
    nearest_area:str
    category:PropertyCategory
    property_type:ProperyType = ProperyType.EVCA_Affiliate
    airport:Optional[bool] = False
    breakfast:Optional[bool] = False
    lunch:Optional[bool] = False
    dinner:Optional[bool] = False
    wifi:Optional[bool] = False
    maximum_security:Optional[bool] = False
    two_showers:Optional[bool] = False
    luxury_bedroom:Optional[bool] = False
    kitchen:Optional[bool] = False
    availability:Optional[bool] = True
    approval_status:Optional[bool] = False
    price:Optional[int]
    capacity:Optional[int]
    discount: List[Link[ApplicableDiscount]] = None
    booking_count:Optional[int] = 0
    owner_id: PydanticObjectId
    image: Optional[List[Link[PropertyImages]]] = None
    video: Optional[List[Link[PropertyVideos]]] = None
    
    class Settings:
        name = "properties"
        

    
class PropertySchema(BaseModel):
    name: str
    description:str
    nearest_area:str
    category:PropertyCategory
    airport:Optional[bool] = False
    breakfast:Optional[bool] = False
    lunch:Optional[bool] = False
    dinner:Optional[bool] = False
    wifi:Optional[bool] = False
    maximum_security:Optional[bool] = False
    two_showers:Optional[bool] = False
    luxury_bedroom:Optional[bool] = False
    kitchen:Optional[bool] = False
    price:str
    capacity:Optional[int]
    discount: Optional[List[ApplicableDiscount]]
    images:Optional[list] = None
    videos:Optional[list] = None
        