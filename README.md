django-email-db
===============

Yet another django Email backend for storing messages in the database.

Configuration
-------------

Add `django_email_db` to your `settings.py`'s `INSTALLED_APPS` and define the Email backend as such:

    EMAIL_BACKEND = 'django_email_db.backend.DBBackend'
    
The `DBBackend` actually uses Django's `django.core.mail.smtp.EmailBackend` so make sure you define:

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'user@gmail.com'
    EMAIL_HOST_PASSWORD = 'secret'
    
Now run:

    manage.py syncdb
    manage.py migrate
    
You can view and send messages from the Admin and you can send any message that hasn't been sent yet with a management command:

    manage.py send
    
If you use virtualenv and you want to execute the management command from your crontab, use the following example:

    ***** root echo 'source /env/bin/activate; python /src/manage.py send' | /bin/bash
  
    
Feel free to fork and improve :)
