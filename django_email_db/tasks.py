from __future__ import absolute_import

from django.core.mail import get_connection
from django.utils.timezone import now

import datetime

from .management.commands.send_messages import get_messages
from .models import Message


try:

    from celery import shared_task
    
    @shared_task
    def send_email_batch():
        get_connection().send_messages_smtp(get_messages())


    @shared_task
    def archive_messages():
        six_months_ago = now() - datetime.timedelta(days=180)
        Message.objects.select_related('attachments').filter(
            created__lte = six_months_ago
        ).delete()


except ImportError:
    pass