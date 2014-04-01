# base class for Message filters

class MessageFilter(object):
    def on_new_message(self, message):
        raise NotImplemented((
            'Must implement on_new_message '
            'and return the (altered) message.'
        ))