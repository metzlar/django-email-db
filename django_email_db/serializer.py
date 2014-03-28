# copied & modified from https://raw.githubusercontent.com/CodeScaleInc/django-gearman-proxy/master/django_gearman_proxy/serializers/mail/json.py


from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.utils.importlib import import_module


def to_dict(email_message):
    result = {}
    for k in dir(email_message):
        if not k[0] == '_':
            att = getattr(email_message, k)
            try:
                result[k] = att
            except TypeError:
                pass
    
    result['attachments'] = email_message.attachments

    return result
    

def from_dict(serialized):

    serialized['connection'] = get_connection()    
    
    cls = EmailMessage
    if 'message_type' in serialized:
        module, klass = serialized['message_type'].split(':')
        cls = getattr(
            import_module(module),
            klass)
        del serialized['message_type']

    attachments = []
    if 'attachments' in serialized:
        attachments = serialized['attachments']
        del serialized['attachments']

    unknown_attrs = {}
    if 'unknown_attrs' in serialized:
        unknown_attrs = serialized['unknown_attrs']
        del serialized['unknown_attrs']

    result = cls(**serialized)

    for k, v in unknown_attrs.iteritems():
        setattr(result, k, v)

    for a in attachments:
        result.attachments.append(a.document)

    return result