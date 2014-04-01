# Example Email filter

from django_email_db.filter import MessageFilter

from random import randint
import sys


class LowPrioError(MessageFilter):
    '''
    This filter changes the priority of Django errors to -100
    '''
    def on_new_message(self, message):
        if message.subject.startswith(
            '[Django] ERROR: Invalid HTTP_HOST header:'
        ):
            message.priority = -100
        return message


class PrioRandom(MessageFilter):
    '''
    This filter changes the priority at random.
    '''
    def on_new_message(self, message):
        if message.priority == 0:
            message.priority = randint(-sys.maxint-1, sys.maxint)
        return message