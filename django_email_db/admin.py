from __future__ import absolute_import

from django.contrib import admin
from django.db import transaction
from django.utils.timezone import now
from django.core.mail import get_connection

from .models import Message, MessageAttachment
from .serializer import from_dict


class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment

    
class MessageAdmin(admin.ModelAdmin):

    actions = ['re_send', 're_schedule']

    @transaction.atomic
    def re_schedule(self, request, queryset):
        queryset.update(sent = None)
        self.message_user(
            request,
            'Selected messages are scheduled to be resent.'
        )
        
    re_schedule.short_description = '(Re-)schedule selected'
    
    @transaction.atomic
    def re_send(self, request, queryset):
        queryset = queryset.select_for_update()
        msgs = [from_dict(m.serialized()) for m in queryset]

        queryset.update(sent = now())

        amount = get_connection().send_messages_smtp(msgs)

        self.message_user(request, '%s were (re)send.' % amount)

    re_send.short_description = '(Re-)send selected'
    
    inlines = [
        MessageAttachmentInline,
    ]

    list_display = ('created', 'to', 'subject', 'priority', 'sent')

    
admin.site.register(Message, MessageAdmin)