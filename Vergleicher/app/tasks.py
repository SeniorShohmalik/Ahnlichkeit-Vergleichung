from app.models import Y_ISH
from celery import shared_task
from time import sleep
from random import random
@shared_task
def count_widgets():
    return random()
