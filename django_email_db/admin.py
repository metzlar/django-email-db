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

    actions = ['re_send']
    
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

    list_display = ('to', 'subject', 'sent')

admin.site.register(Message, MessageAdmin)