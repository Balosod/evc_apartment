from fastapi_mail import FastMail, MessageSchema, ConnectionConfig,MessageType
from pydantic import EmailStr, BaseModel
from ..settings import CONFIG_SETTINGS
from ..settings import conf
import pyotp
from jinja2 import Environment, select_autoescape, PackageLoader

mail_env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)



fm = FastMail(conf)

class OTPManager:
    totp = pyotp.TOTP(CONFIG_SETTINGS.OTP_SECRET_KEY, interval=int(CONFIG_SETTINGS.OTP_EXPIRES), digits=int(CONFIG_SETTINGS.OTP_DIGIT))

    @classmethod
    def generate(cls):
        return cls.totp.now()

    @classmethod
    def verify(cls, otp: str):
        status = cls.totp.verify(otp)
        return status


class EmailManager:
    @staticmethod
    def send_welcome_msg(email):
        otp = OTPManager.generate()
        return EmailManager.dispatch(email=email, message_type="welcome", otp=otp)

    @staticmethod
    def send_otp_msg(email):
        otp = OTPManager.generate()
        return EmailManager.dispatch(email=email, message_type="otp", otp=otp)

    @staticmethod
    def dispatch(email, message_type, otp=None):
        MSG_TYPES = {
            "welcome": {
                "subject": "EVC_Apartment: Verify your account",
                "template": "welcome",
                "message": f"Hi there, welcome to your account. Use this OTP to continue: {otp}."
            },
            "otp": {
                "subject": "EVC_Apartment: OTP Verification",                           
                "template": "otp",
                "message": f"Hi there, to verify your action, kindly use this OTP to continue: {otp}."
            }
        }

        if not message_type in MSG_TYPES.keys():
            print(f"Invalid message type. Choose from {MSG_TYPES.keys()}")

        subject = MSG_TYPES[message_type]["subject"]
        template = MSG_TYPES[message_type]["template"]
        plain_message = MSG_TYPES[message_type]["message"]
        
        template = mail_env.get_template(f'{template}.html')
        
        html = template.render(
                email= email,
                subject=subject,
                otp=otp if otp else ''
        )
        
        message = MessageSchema(
        subject=subject,
        recipients=[email], 
        body=html,
        subtype=MessageType.html
        )
        return message

