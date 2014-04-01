from __future__ import absolute_import

from django.db import models
from django.utils.importlib import import_module

from .serializer import to_dict

import os, sys


json = import_module('json')


class Message(models.Model):
    
    ### EmailMessage fields
    subject = models.CharField(
        max_length=255, null = True, blank = True)
    body = models.TextField(null = True, blank = True)
    from_email = models.CharField(max_length = 255)
    to = models.TextField()
    bcc = models.TextField(null = True, blank = True)
    cc = models.TextField(null = True, blank = True)
    headers = models.TextField(null = True, blank = True)

    ### Meta data
    message_type = models.TextField()
    unknown_attrs = models.TextField(null = True, blank = True)
    missed_attrs = models.TextField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    sent = models.DateTimeField(null = True)
    # priority, 0 is average, >0 is hight prio, <0 is low prio
    priority = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode("%s:%s (%s) %s" % (
            json.loads(self.to),
            json.loads(self.subject),
            json.loads(self.from_email),
            str(self.sent or 'NOT YET SENT')
        ))

    def serialized(self):
        field_names = [
            'subject',
            'body',
            'from_email',
            'to',
            'bcc',
            'cc',
            'headers'
        ]
        result = {}
        for n in field_names:
            attr = getattr(self, n)
            if attr:
                try:
                    result[n] = json.loads(str(attr))
                except ValueError:
                    print >> sys.stderr, (
                        'WARNING, could not json.loads ',
                        str(attr)
                    )
            else:
                result[n] = None

        result['message_type'] = self.message_type
        result['unknown_attrs'] = json.loads(self.unknown_attrs)
        print >> sys.stderr, (
            'WARNING, missed attrs while serializing ',
            self.missed_attrs)

        result['attachments'] = []
        for a in self.attachments.all():
            result['attachments'].append(a)
        
        return result
        
    @classmethod
    def save_from_message(cls, message):
        dict_ = to_dict(message)
        attachments = []
        if 'attachments' in dict_:
            attachments = dict_['attachments']
            del dict_['attachments']

        result = cls()

        unknown_attrs = {}
        missed_attrs = []
        for k in dict_.keys():
            v = None
            try:
                v = json.dumps(dict_[k])
            except:
                pass
                
            if hasattr(result, k):
                setattr(result, k, v)
            elif v:
                unknown_attrs[k] = dict_[k]
            else:
                missed_attrs.append(k)

        result.unknown_attrs = json.dumps(unknown_attrs)
        result.missed_attrs = json.dumps(missed_attrs)
        result.message_type = (
            message.__class__.__module__ + ':' +
            message.__class__.__name__
        )

        # no circular import 
        from .backend import MessageFilters
        result = MessageFilters.new_message(result)
        
        result.save()

        for a in attachments:
            MessageAttachment(
                document = a,
                message = result
            ).save()

        return result
    

class MessageAttachment(models.Model):
    message = models.ForeignKey(
        Message,
        related_name='attachments'
    )
    headers = models.TextField(null=True, blank=True)
    document = models.FileField(
        upload_to=lambda instance, filename: os.path.join(
            ['attachments', str(instance.pk), filename]))