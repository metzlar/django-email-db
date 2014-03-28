# copied & modified from https://raw.githubusercontent.com/CodeScaleInc/django-gearman-proxy/master/django_gearman_proxy/serializers/mail/json.py


from django.core.mail import get_connection
from django.core.mail.message import EmailMessage


def serialize(email_message):

    return {
        'subject': email_message.subject,
        'body': email_message.body,
        'from_email': email_message.from_email,
        'to': email_message.to,
        'bcc': email_message.bcc,
        'attachments': email_message.attachments,
        'headers': email_message.extra_headers,
        'cc': email_message.cc,
    }


def unserialize(serialized):

    return EmailMessage(
        subject =serialized.get('subject', u''),
        body =serialized.get('body', u''),
        from_email =serialized.get('from_email'),
        to = serialized.get('to'),
        bcc = serialized.get('bcc'),
        attachments = serialized.get('attachments'),
        headers = serialized.get('headers'),
        cc = serialized.get('cc'),
        connection = get_connection(),
    )