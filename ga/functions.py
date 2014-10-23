import os
from django.db import connection
from ga import settings


def prefetch_id(instance):
    """ Fetch the next value in a django id autofield postgresql sequence """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT nextval('{0}_{1}_id_seq'::regclass)".format(
            instance._meta.app_label.lower(),
            instance._meta.object_name.lower(),
        )
    )
    row = cursor.fetchone()
    cursor.close()
    return int(row[0])

def upload_path(instance, filename):
    unused, extension = os.path.splitext(filename)
    return '/'.join([settings.MEDIA_ROOT, instance.__class__.__name__, ("%s%s" % (instance.id, extension))])


def postmark_email(subject, to_address, body, tag):
    from postmark import PMMail
    message = PMMail(
         api_key = settings.POSTMARK_API_KEY,
         subject = subject,
         sender = "grimes@grimesengineering.com",
         bcc = "dillon.grimes@gmail.com",
         to = to_address,
         text_body = body,
         tag = tag
    )
    message.send()