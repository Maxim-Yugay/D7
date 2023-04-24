from celery import shared_task
import datetime, time
from news_paper.models import Post
from django.core.mail import send_mail


def my_job():
    user = super().user()
    post = Post.objects.order_by('dateCreations')[:10]
    text = '\n'.join(['{} - {}'.format(p.name, p.post) for p in post])
    mail_send = send_mail(
        subject= 'Последние посты',
        messsage= text,
        recipient_list=user,
    )
    return mail_send

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)



