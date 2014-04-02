from __future__ import absolute_import

from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from django.utils.importlib import import_module

from .models import Message
from .filter import MessageFilter

import sys


class MessageFilters(object):

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance._filters = None
        return cls._instance
    
    def get_filters(self):
        if self._filters is None:
            self._filters = collect_filters()
        return self._filters
    filters = property(get_filters)
    
    @classmethod
    def new_message(cls, message):
        for filter in cls().filters:
            message = filter.on_new_message(message)
        return message

        
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


def collect_filters():
    result = []
    for a in settings.INSTALLED_APPS:
        filter_module = None
        try:
            filter_module = import_module(
                '%s.email_db_filters' % a
            )
        except ImportError:
            pass
        if not filter_module is None:
            for k in dir(filter_module):
                test = getattr(filter_module, k)
                try:
                    if (
                        issubclass(test, MessageFilter) and
                        not test is MessageFilter
                    ):
                        result.append(test())
                except:
                    pass
    return result