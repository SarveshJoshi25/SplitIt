from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage
from config import EmailAddress, EmailPassword, AccessSecretKey
from .authorization.serializers import UserSerializer
from celery import shared_task


def create_validator_for_email(user_id):
    return UserSerializer.fetch_user(user_id)


@shared_task
def send_verification_email(user_id):
    print("here")
    user = UserSerializer.fetch_user(user_id)
    message = get_template("verification_email.html").render({
        'confirmation_link': "http://localhost:8000" + '/split_it/api/v1/authenticate/verify/' +
                             create_validator_for_email(user.user_id).user_id})

    mail = EmailMessage(
        subject="Verify your SplitIT account",
        body=message,
        from_email=EmailAddress,
        to=[user.email_address],
        reply_to=[EmailAddress],
    )
    mail.content_subtype = "html"
    mail.send()
    return "Email sent to " + user.email_address
