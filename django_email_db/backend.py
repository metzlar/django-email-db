from __future__ import absolute_import

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

from .models import EmailMessage

import sys


class DBBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        count = 0
        for message in email_messages:
            try:
                entry = EmailMessage.from_message(message)
                entry.save()
                count += 1
            except:
                if settings.DEBUG:
                    print >> sys.stderr, 'MESSAGE', message
                    import traceback
                    traceback.print_exc()
                    pass
        return count