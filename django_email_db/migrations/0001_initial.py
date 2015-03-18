# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_email_db.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('from_email', models.CharField(max_length=255)),
                ('to', models.TextField()),
                ('bcc', models.TextField(null=True, blank=True)),
                ('cc', models.TextField(null=True, blank=True)),
                ('headers', models.TextField(null=True, blank=True)),
                ('message_type', models.TextField()),
                ('unknown_attrs', models.TextField(null=True, blank=True)),
                ('missed_attrs', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField(null=True)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headers', models.TextField(null=True, blank=True)),
                ('document', models.FileField(upload_to=django_email_db.models.attachment_upload_to)),
                ('message', models.ForeignKey(related_name='attachments', to='django_email_db.Message')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
