from celery_tasks.main import app
from django.core.mail import send_mail


@app.task
def celery_send_emails(subject, message, from_email, recipient_list,html_message):
    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=recipient_list,
              html_message=html_message)
