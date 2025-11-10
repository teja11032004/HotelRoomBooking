import uuid
from django.core.mail import send_mail
from django.conf import settings

def generateToken():
    return str(uuid.uuid4())


def sendEmailToken(email,token):
    subject="Verify your email adress"
    message=f"""Please Verify you email account by clicking this link
            http://127.0.0.1:8000/accounts/verify-accounts/{token}/

    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
)

