from __future__ import absolute_import

from django.db import models


class Message(models.Model):
    subject = models.CharField(
        max_length=255, null = True, blank = True)
    body = models.TextField(null = True, blank = True)
    from_email = models.CharField(max_length=255)
    to = models.TextField()
    bcc = models.TextField(null = True, blank = True)
    cc = models.TextField(null = True, blank = True)
    headers = models.TextField(null=True, blank=True)


class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message,
        related_name='attachments'
    )
    headers = models.TextField(null=True, blank=True)
    document = models.FileField()