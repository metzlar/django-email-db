from __future__ import absolute_import

from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

from .models import Message

import sys


class DBBackend(EmailBackend):
    def send_messages_smtp(self, *args, **kwargs):
        return super(
            DBBackend, self
        ).send_messages(*args, **kwargs)
    
    def send_messages(self, email_messages):
        count = 0
        for message in email_messages:
            try:
                Message.save_from_message(message)
                count += 1
            except:
                if settings.DEBUG:
                    print >> sys.stderr, 'MESSAGE', message
                    import traceback
                    traceback.print_exc()
                    pass
        return count