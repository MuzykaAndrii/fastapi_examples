from fastapi import APIRouter, Depends

from tasks.tasks import send_letter
from config import settings


router = APIRouter(
    prefix="/send",
    tags=["Mailing"],
)


# @router.get("/simple")
# def send_simple_email(user=Depends(current_user)):
#     send_letter.delay(settings.SMTP_USER, f"Hello, world! <br> P.s. from {user.username}")
#     return {
#         "status": 200,
#         "data": "email sent successfully",
#         "details": None,
#     }
