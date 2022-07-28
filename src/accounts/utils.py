from os import getenv

from django.core.mail import send_mail

import environ
env = environ.Env()
environ.Env.read_env()

from django.core.signing import Signer
from django.template.loader import render_to_string

signer = Signer()




def send_activation_notification(user):


    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = bool(getenv("DEBUG", default=True))

    ALLOWED_HOSTS = getenv('ALLOWED_HOSTS').split()

    if ALLOWED_HOSTS:
        host = f'http://{ALLOWED_HOSTS[0]}'
    else:
        host = 'http://localhost:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}

    subject = render_to_string('email/activation_letter_subject.txt', context)
    body = render_to_string('email/activation_letter_body.txt', context)

    # user.email_user(subject, body)

    user_email = user.email
    send_mail(
        subject,
        body,
        env("EMAIL_HOST_USER").EMAIL_HOST_USER,
        [user_email],
        fail_silently=True
    )
