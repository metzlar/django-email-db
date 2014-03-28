from __future__ import absolute_import

from django.core.mail import get_connection
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now

from django_email_db.models import Message
from django_email_db.serializer import from_dict


class Command(BaseCommand):

    @transaction.atomic
    def get_messages(self):
        messages = Message.objects.select_for_update().filter(
            sent__isnull = True
        )

        result = [from_dict(m.serialized()) for m in messages]

        messages.update(sent = now())

        self.stderr.write('Going to send %s messages: %s' % (
            str(len(result)),
            str(result)
        ))
        
        return result
        
    
    def handle(self, *args, **options):
        self.stdout.write(
            'Sent messages: %s' % get_connection(
            ).send_messages_smtp(
                self.get_messages()
            )
        )