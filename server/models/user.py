from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field,validator
from datetime import date
from enum import Enum

today = date.today()

class accountType(str,Enum):
    personal_account = "personal"
    cooperate_account = "corporate"
    
class User(Document):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio:Optional[str] = None
    email: EmailStr
    phone:Optional[str] = None
    address:Optional[str] = None
    img:Optional[str] = None
    password: str
    account_type:Optional[accountType] = None
    is_admin:bool = False
    is_affiliate:bool = False
    created:str = today.strftime("%B %d, %Y")
    active: bool = False
    
    @validator('password', always=True)
    def validate_password(cls, password):
        
        min_length = 8
        errors = ''
        if len(password) < min_length:
            errors += 'Password must be at least 8 characters long. '
        if not any(character.islower() for character in password):
            errors += 'Password should contain at least one lowercase character.'
        if errors:
            raise ValueError(errors)
            
        return password
    

    class Settings:
        name = "users"

    

   
class UserRegistrationSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone:Optional[str] = None
    password: str
    account_type:Optional[accountType] = None

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example" : {
                "email": "johndoe@mail.com",
                "password": "yoursecretpa55word",
            }
        }
        
        
class UserOut(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    email: EmailStr
    phone: Optional[str]
    address: Optional[str]
    img: Optional[str]
    account_type: Optional[str]
    is_admin: bool
    is_affiliate: bool 
    created: str 
    active: bool


class UserCollection(BaseCollectionModel[UserOut]):
    pass
    
class OtpSchema(BaseModel):
    email: EmailStr = Field(...)
    otp: str = Field(...)
    
    
class EmailSchema(BaseModel):
    email: EmailStr = Field(...)
    

class ImageSchema(BaseModel):
    image: str
    
class ProfileDataSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone:Optional[str] = None
    address:Optional[str] = None
    bio:Optional[str] = None
    
    
    

def SuccessResponseModel(data, code, message):
    return { "data": [data], "code": code, "message": message }


def ErrorResponseModel(error, code, message):
    return { "error": error, "code": code, "message": message }