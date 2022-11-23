from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail

from .models import Message, Chat


@shared_task
def notify_message_not_read():
    messages = Message.objects.filter(is_read=False).order_by('-creation_date')
    date_time_format = "%d/%m/%Y %H:%M:%S"

    time_now = datetime.now().strftime(date_time_format)
    time_now_date = datetime.strptime(time_now, date_time_format)

    for message in messages.all():
        message_created = message.creation_date.strftime(date_time_format)
        message_created_date = datetime.strptime(message_created, date_time_format)
        delta = time_now_date - message_created_date

        if (delta.days) < 1:
            chat = message.chat
            users = chat.chat_members.filter().exclude(nickname=message.user.nickname)
            for user in users.all():

                send_mail(
                    subject=f'Здравствуйте, {user.nickname}. У вас больше суток не прочитано сообщение в чате {message.chat.name}!',
                    message=f'Перейти в чат {message.chat.name}: http://127.0.0.1:8000/chat/{message.chat.name}',
                    from_email='alexvgutnik@yandex.ru',
                    recipient_list=[user.mail],
                )


@shared_task
def new_message(instance):
    message = instance.text[:20] + '...'
    print(message)