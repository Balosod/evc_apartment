from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from decouple import config
from pydantic import BaseModel
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType



class Settings(BaseModel):
    
    #Auth Setting
    authjwt_secret_key = config("SECRET")
    authjwt_access_token_expires = 86400
    authjwt_algorithm = config("ALGORITHM")
    
    #Database Setting
    DATABASE_URL = config("DATABASE_URL")
    DATABASE_NAME = config("DATABASE_NAME")

    #OTP Setting
    OTP_SECRET_KEY=config("OTP_SECRET_KEY")
    OTP_EXPIRES=config("OTP_EXPIRES")
    OTP_DIGIT=config("OTP_DIGIT")
    
    #Social Auth Setting
        #google
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
        #facebook
    SOCIAL_AUTH_FACEBOOK_KEY=config("SOCIAL_AUTH_FACEBOOK_KEY")
    SOCIAL_AUTH_FACEBOOK_SECRET=config("SOCIAL_AUTH_FACEBOOK_SECRET")
    
    #S3 Bucket setting
    USE_SPACES=True
    REGION_NAME=config("REGION_NAME")
    ENDPOINT_URL=config("ENDPOINT_URL")
    AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY")
    BUCKET=config("BUCKET")
    ACL=config("ACL")
    


conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = 465,
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS = True,
)
 
CONFIG_SETTINGS = Settings()




