import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import settings

# celery -A tasks.tasks:celery worker --loglevel=INFO
# celery -A tasks.tasks:celery flower --loglevel=INFO


celery = Celery("tasks", broker=settings.redis_url)


def create_email_letter(recipient: str, content: str):
    letter = EmailMessage()

    letter["subject"] = "Some subject"
    letter["From"] = settings.SMTP_USER
    letter["To"] = recipient
    letter.set_content(content, subtype="html")

    return letter


def send_email(letter: EmailMessage):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp_server:
        smtp_server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp_server.send_message(letter)


@celery.task
def send_letter(recipient: str, content: str):
    letter = create_email_letter(recipient, content)
    send_email(letter)
