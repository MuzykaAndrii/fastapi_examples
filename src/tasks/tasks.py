import smtplib
from email.message import EmailMessage

from celery import Celery
from config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    REDIS_HOST,
    REDIS_PORT,
)

# celery -A tasks.tasks:celery worker --loglevel=INFO
# celery -A tasks.tasks:celery flower --loglevel=INFO


celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

def create_email_letter(recipient: str, content: str):
    letter = EmailMessage()

    letter['subject'] = "Some subject"
    letter['From'] = SMTP_USER
    letter['To'] = recipient
    letter.set_content(content, subtype='html')

    return letter


def send_email(letter: EmailMessage):
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp_server:
        smtp_server.login(SMTP_USER, SMTP_PASSWORD)
        smtp_server.send_message(letter)


@celery.task
def send_letter(recipient: str, content: str):
    letter = create_email_letter(recipient, content)
    send_email(letter)
