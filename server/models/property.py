from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from beanie import Document, Link,PydanticObjectId
from pydantic import BaseModel, EmailStr, Field,validator
from enum import Enum


class AirportOptions(str,Enum):
    yes = "yes"
    no = "no"

class ProperyType(str,Enum):
    EVC_Apartment = "EVC_Apartment"
    EVCA_Affiliate = "EVCA_Affiliate"
    
class ProperyCondition(str,Enum):
    Available = "Available"
    Occupied = "Occupied"

class ProperyStatus(str,Enum):
    Approve = "Approve"
    Reject = "Reject"
    
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
    #airport:Optional[AirportOptions] = AirportOptions.no
    airport:Optional[bool] = False
    breakfast:Optional[bool] = False
    lunch:Optional[bool] = False
    dinner:Optional[bool] = False
    discount: List[Link[ApplicableDiscount]] = None
    food_option:Optional[list] = None
    services:Optional[list] = None
    condition:Optional[ProperyCondition] = ProperyCondition.Available
    status:Optional[ProperyStatus] = ProperyStatus.Reject
    order:Optional[int] = 0
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
    #airport:Optional[AirportOptions] = AirportOptions.no
    airport:Optional[bool] = False
    breakfast:Optional[bool] = False
    lunch:Optional[bool] = False
    dinner:Optional[bool] = False
    discount: Optional[List[ApplicableDiscount]]
    food_option:list
    services:list
    images:Optional[list] = None
    videos:Optional[list] = None
        