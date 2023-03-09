from fastapi import HTTPException
from .helpers import EmailManager, OTPManager
from ..utils.helpers import api_instance
from ..models.user import User


async def verify_OTP(email: str, otp: str):
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=400, detail="This email is invalid.")
    if not OTPManager.verify(otp):
        raise HTTPException(
            status_code=400, detail="This otp is invalid or has expired."
        )
    user.active = True
    await user.save()
    return "success"


async def resend_OTP(email: str):
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=400, detail="This email is invalid.")
    try:
        send_smtp_email = EmailManager.send_otp_msg(user.email)
        api_response = api_instance.send_transac_email(send_smtp_email)
        return "success"

    except:
        return HTTPException(status_code=400, detail="Mail not send")
