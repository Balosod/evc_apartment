from fastapi import APIRouter, Depends,HTTPException
from starlette.requests import Request
from fastapi_sso.sso.google import GoogleSSO 
from fastapi_sso.sso.facebook import FacebookSSO
from server.models.user import User,ErrorResponseModel
from fastapi_jwt_auth import AuthJWT
from ..settings import CONFIG_SETTINGS

#https://postatusbackend.getrapidmvp.com/
#http://127.0.0.1:8000/
#https://postatusbackend.getrapidmvp.com/social/auth/facebook/callback
router = APIRouter()

google_sso = GoogleSSO(CONFIG_SETTINGS.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, CONFIG_SETTINGS.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET, "https://evcabackend.getrapidmvp.com/social/auth/google/callback",use_state=False)
facebook_sso = FacebookSSO(CONFIG_SETTINGS.SOCIAL_AUTH_FACEBOOK_KEY, CONFIG_SETTINGS.SOCIAL_AUTH_FACEBOOK_SECRET , "http://127.0.0.1:8000/social/auth/facebook/callback",use_state=False)

@router.get("/auth/google/login")
async def google_login():
    return await google_sso.get_login_redirect()


@router.get("/auth/google/callback")
async def google_callback(request: Request,Authorize: AuthJWT = Depends()):
    """Process login response from Google and return user info"""
    try:
        user = await google_sso.verify_and_process(request)
        print(user)
        if user is None:
            raise HTTPException(401, "Failed to fetch user information")
        user_exists = await User.find_one(User.email == user.email)
        if user_exists:
            access_token = Authorize.create_access_token(subject=user.email)
            refresh_token = Authorize.create_refresh_token(subject=user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            user_obj = User(
            email=user.email,
            first_name = user.last_name,
            last_name = user.first_name,
            password=user.email,
            active = True
            )
            await user_obj.create() 
            access_token = Authorize.create_access_token(subject=user.email)
            refresh_token = Authorize.create_refresh_token(subject=user.email)
            return {"access_token": access_token, "refresh_token": refresh_token}
    except:
        return ErrorResponseModel("Timeout Error", 401, "Timeout Error" )
    
    
# @router.get("/auth/facebook/login")
# async def facebook_login():
#     return await facebook_sso.get_login_redirect()


# @router.get("/auth/facebook/callback")
# async def facebook_callback(request: Request,Authorize: AuthJWT = Depends()):
#     """Process login response from facebook and return user info"""
#     try:
#         user = await facebook_sso.verify_and_process(request)
#         print(user)
#         if user is None:
#             raise HTTPException(401, "Failed to fetch user information")
#         user_exists = await User.find_one(User.email == user.email)
#         if user_exists:
#             access_token = Authorize.create_access_token(subject=user.email)
#             refresh_token = Authorize.create_refresh_token(subject=user.email)
#             return {"access_token": access_token, "refresh_token": refresh_token}
#         else:
#             user_obj = User(
#             email=user.email,
#             firstname = user.first_name,
#             lastname = user.last_name,
#             password=user.email,
#             interest=[],
#             provider=user.provider,
#             active = True
#             )
#             await user_obj.create() 
#             access_token = Authorize.create_access_token(subject=user.email)
#             refresh_token = Authorize.create_refresh_token(subject=user.email)
#             return {"access_token": access_token, "refresh_token": refresh_token}
#     except:
#         return ErrorResponseModel("Timeout Error", 401, "Timeout Error" )