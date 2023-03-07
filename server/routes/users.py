from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends,Response
from passlib.context import CryptContext
from typing import List
import re
import base64
import uuid
from ..utils import auth_service
from ..utils.helpers import api_instance
from ..utils.helpers import EmailManager
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS
from pydantic import BaseModel
from starlette.responses import JSONResponse

# from auth.auth_handler import signJWT
from fastapi_jwt_auth import AuthJWT


from server.models.user import (
    User,
    UserRegistrationSchema,
    UserLogin,
    UserOut,
    OtpSchema,
    ImageSchema,
    ProfileDataSchema,
    EmailSchema,
    SuccessResponseModel,
    UserCollection,
    ErrorResponseModel
)



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def user_data(user):
    return {"id":user.id,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "bio":user.bio,
            "email":user.email,
            "phone":user.phone,
            "address":user.address,
            "img":user.img,
            "account_type":user.account_type,
            "is_admin":user.is_admin,
            "is_affiliate":user.is_affiliate,
            "created":user.created,
            "active":"user.active"}
    
    

@router.get("/all", status_code=200)
async def get_all_user() -> dict:
    all_users = await User.find_all().to_list()
    users_out = UserCollection(all_users)
    total_users = len(users_out)
    return {"data": {"count": total_users, "items": users_out}}


@router.delete("/delete/{ID}", status_code = 200)
async def delete_a_user(ID:PydanticObjectId,response:Response) -> dict:
    try:
        user = await User.find_one(User.id==ID, fetch_links=True)
        await user.delete()
        return{"message":f"user with ID: {ID} successfully deleted"}
    except:
        response.status_code = 400
        return {"message":"something went wrong! or empty user list"}
    
    
@router.post("/signup", response_description="User added to the database",status_code=201)
async def create_account(data: UserRegistrationSchema,response:Response) -> dict:
    
    email_regex = r'com$'
    match = re.search(email_regex, data.email)
    if not match:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email is invalid"
        )
        
    email_exists = await User.find_one(User.email == data.email)

    if email_exists:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Email already exists!"
        )
    phone_exists = await User.find_one(User.phone == data.phone)
    
    if phone_exists:
        response.status_code = 400
        return HTTPException(
            status_code=400,
            detail="Phone number already exists!"
        )

    hash_password = pwd_context.hash(data.password)
    
    user = User(
        first_name = data.first_name,
        last_name = data.last_name,
        email = data.email,
        phone = data.phone,
        password = hash_password,
        account_type = data.account_type
    )
    try:
        send_smtp_email  = EmailManager.send_welcome_msg(data.email)
        api_response = api_instance.send_transac_email(send_smtp_email)
        await user.create()
        return SuccessResponseModel(user_data(user), 201, "successful" )
    
    
    except:
        return HTTPException(
            status_code=400,
            detail="User not created"
        )


@router.post("/auth/login", response_description="User login",status_code = 200)
async def login_user(user: UserLogin, response:Response, Authorize: AuthJWT = Depends()):
    user_acct = await User.find_one(User.email == user.email)
    try:
        if user_acct and user_acct.active and pwd_context.verify(user.password, user_acct.password):
            access_token = Authorize.create_access_token(subject=user.email)
            refresh_token = Authorize.create_refresh_token(subject=user.email)
            return {"access_token": access_token, "refresh_token": refresh_token,"user_data":user_data(user_acct)}

        response.status_code = 400
        return HTTPException(
                status_code=400,
                detail="Incorrect email or password"
            )
    except:
        response.status_code = 400
        return HTTPException(
                status_code=400,
                detail="Invalid email or Password"
            )


@router.post("/refresh", response_description="Get new access token")
def get_new_access_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.post("/auth/verify", response_description="verify otp", status_code = 200)
async def verify_otp(data: OtpSchema):
    
    obj = await auth_service.verify_OTP(data.email,data.otp)
    return {"message":obj}


@router.post("/auth/resend", response_description="resend otp",status_code = 200)
async def resend_otp(data:EmailSchema):

    obj = await auth_service.resend_OTP(data.email)
    return {"message":obj}



@router.get("/profile",status_code = 200)
async def get_user_profile_data(response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        return user
    else:
        response.status_code = 400
        return{"message":"User not found"}



@router.post("/profile/image/update", status_code = 200, response_description="Upload profile image")
async def upload_profile_image(data:ImageSchema, response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if CONFIG_SETTINGS.USE_SPACES:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            client.put_object(
            Bucket=CONFIG_SETTINGS.BUCKET,
            Body=img_recovered,
            Key=f"image/{img_name}",
            ACL=CONFIG_SETTINGS.ACL,
            ContentType="image/png"
            )
                
            img_url = f"https://postatusapistorage.nyc3.digitaloceanspaces.com/image/{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded."}
        else:
            img_name = str(uuid.uuid4())[:10] + '.png'
            image_as_bytes = str.encode(data.image) 
            img_recovered = base64.b64decode(image_as_bytes)
            
            with open("server/media/image/uploaded_" + img_name, "wb") as f:
                f.write(img_recovered)
                
            img_url = f"http://localhost:8000/media/image/uploaded_{img_name}"
            
            user.img = img_url
            await user.save()
            
            return{"message":"image successfully uploaded"}
    else:
        response.status_code = 400
        return{"message":"User not found"}
    

@router.put("/profile/update", status_code = 200, response_description="data updated")
async def update_profile_data(data:ProfileDataSchema, response:Response, Authorize: AuthJWT = Depends()):
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    user = await User.find_one(User.email == current_user)
    if user:
        if (data.first_name and data.first_name != ""):
            user.first_name = data.first_name
        if (data.last_name and data.last_name != ""):
            user.last_name = data.last_name
        if (data.email and data.email != ""):
            email_regex = r'com$'
            match = re.search(email_regex, data.email)
            if not match:
                response.status_code = 400
                return HTTPException(
                    status_code=400,
                    detail="Email is invalid"
                )
            user.email = data.email
        if (data.phone and data.phone != ""):
            user.phone = data.phone
        if (data.address and data.address != ""):
            user.address = data.address
        if (data.bio and data.bio != ""):
            user.bio = data.bio
        await user.save()
        return {"message":"Data successfully updated"}
    else:
        response.status_code = 400
        return{"message":"User not found"}
    