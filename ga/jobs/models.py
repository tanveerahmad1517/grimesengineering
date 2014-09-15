from django.db import connection, models
from ga.jobs.util import STATE_CHOICES
from ga.services.models import Department
from ga.about.models import Staff
from ga import settings
import os
from django.template.defaultfilters import slugify

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

class JobStatus(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Job(models.Model):
    number = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True,)
    status = models.ForeignKey(to=JobStatus)
    date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=100, null=True, blank=True,)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True,)
    display = models.BooleanField(default=False)
    department = models.ForeignKey(to=Department, null=True,)
    staff = models.ForeignKey(to=Staff, null=True, blank=True,)
    image = models.ImageField(null=True, blank=True, upload_to = upload_path)
#     thumb = ImageSpecField(
#         source='image',
#         processors=[ResizeToFit(250, 250)],
#         format='JPEG',
#         options={'quality': 60},
#     )
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.number)

    @property
    def slug(self):
        return slugify(self.name)

class JobImage(models.Model):
    job = models.ForeignKey(to=Job, related_name='images')
    image = models.ImageField(upload_to = upload_path)
#     thumb = ImageSpecField(
#         source='image',
#         processors=[ResizeToFit(250, 250)],
#         format='JPEG',
#         options={'quality': 60},
#     )
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id and self.image:
            self.id = prefetch_id(self)

        super(JobImage, self).save(*args, **kwargs)

class JobDocumentManager(models.Manager):
    #===========================================================================
    # CREATE A LIST OF CURRENT JOBS WITH RELATED DOCUMENTS
    #===========================================================================
    def available_documents(self):
        jobs = []
        for item in self.select_related('job').filter(job__id__isnull=False):
            if item.job.status == item.type:
                jobs.append(item.job)
        return jobs

class JobDocument(models.Model):
    job = models.ForeignKey(to=Job, related_name='documents')
    document = models.FileField(upload_to = upload_path)
    type = models.ForeignKey(to=JobStatus)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.document.name)

    def save(self, *args, **kwargs):
        if not self.id and self.document:
            self.id = prefetch_id(self)

        super(JobDocument, self).save(*args, **kwargs)

    objects = JobDocumentManager()

class Client(models.Model):
    name = models.CharField(max_length=100)
    sort = models.FloatField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["sort"]

class DownloadUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    job = models.ForeignKey(to=Job, null=True)
    
class Download(models.Model):
    jobdocument = models.ForeignKey(to=JobDocument)
    downloaduser = models.ForeignKey(to=DownloadUser)