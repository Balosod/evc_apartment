from pydantic import EmailStr, BaseModel
from ..settings import CONFIG_SETTINGS
import pyotp
from jinja2 import Environment, select_autoescape, PackageLoader
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = CONFIG_SETTINGS.SEND_IN_BLUE_API_KEY
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


mail_env = Environment(
    loader=PackageLoader('server', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)




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
        sender = {"name":"EVC_Apartment","email":"evcapartment@gmail.com"}
        replyTo = {"name":"EVC_Apartment","email":"evcapartment@gmail.com"}
        to = [{"email":f"{email}"}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=replyTo,  html_content=html, sender=sender, subject=subject)
        
        return send_smtp_email
        

