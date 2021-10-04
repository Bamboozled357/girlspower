from celery import shared_task

# from time import sleep

from django.core.mail import send_mail

# @shared_task
# def sleepy(duration):
#     sleep(duration)
#     return None
from facelook.celery import app


@app.task
def send_activation_mail(email, activation_code):
    from django.core.mail import send_mail
    message = f'Ваш код активации: {activation_code}'
    send_mail('Активация аккаунта',
              message,
              'test@test.com',
              [email])

