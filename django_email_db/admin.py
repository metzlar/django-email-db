from __future__ import absolute_import

from django.contrib import admin

from .models import Message, MessageAttachment

class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment

class MessageAdmin(admin.ModelAdmin):
    inlines = [
        MessageAttachmentInline,
    ]

admin.site.register(Message, MessageAdmin)