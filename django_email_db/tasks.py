from __future__ import absolute_import

from django.core.mail import get_connection

from .management.commands.send_messages import get_messages


try:

    from celery import shared_task
    
    @shared_task
    def send_email_batch():
        get_connection().send_messages_smtp(get_messages())


except ImportError:
    pass