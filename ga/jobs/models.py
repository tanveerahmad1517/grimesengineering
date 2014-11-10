from django.db import models
from ga.jobs.util import STATE_CHOICES
from ga.services.models import Department
from ga.about.models import Staff
from django.template.defaultfilters import slugify
from ga.functions import upload_path, prefetch_id
import os
from django.core.urlresolvers import reverse
from base64 import b64encode
import datetime
from ga import settings

class JobStatus(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class Job(models.Model):
    number = models.FloatField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True,)
    status = models.ForeignKey(to=JobStatus)
    date = models.DateField(default=datetime.date.today())
    city = models.CharField(max_length=100, null=True, blank=True,)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True,)
    display = models.BooleanField(default=False)
    department = models.ForeignKey(to=Department, null=True,)
    staff = models.ForeignKey(to=Staff, null=True, blank=True,)
#     image = models.ImageField(null=True, blank=True, upload_to = upload_path)
#     thumb = ImageSpecField(
#         source='image',
#         processors=[ResizeToFit(250, 250)],
#         format='JPEG',
#         options={'quality': 60},
#     )
    class Meta:
        ordering = ['-date']
        
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.number)

    @property
    def slug(self):
        return slugify(self.name)
    
    @property
    def url(self):
        return reverse(
            'job:detail', 
            kwargs = {
                'job_id': self.id, 
                'job_slug': self.slug,
            }
        )
    
    @property
    def main_image(self):
        for img in self.images.all()[:1]:
            return img.image
        return None

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

    class Meta:
        ordering = ["date"]

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
            if item.job not in jobs:
                jobs.append(item.job)
        return jobs

class JobDocument(models.Model):
    job = models.ForeignKey(to=Job, related_name='documents')
    document = models.FileField(upload_to = upload_path)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def filename(self):
        return os.path.basename(self.document.name)

    def save(self, *args, **kwargs):
        if not self.id and self.document:
            self.id = prefetch_id(self)

            email_list = []
            for entry in Download.objects.filter(jobdocument__job = self.job):
                if entry.downloaduser.email not in email_list:
                    email_list.append(entry.downloaduser.email)
                    
            message = "A new document has been uploaded for job: %(job_title)s. This new document is available to download from http://www.grimesengineering.com%(job_url)s" % {
                'job_url': self.job.url,
                'job_title': self.job.name,
            }
            from postmark import PMMail
            message = PMMail(
                 api_key = settings.POSTMARK_API_KEY,
                 subject = "Grimes & Associates New Document Uploaded",
                 sender = "grimes@grimesengineering.com",
                 cc = ','.join(email_list),
                 to = "grimes@grimesengineering.com",
                 text_body = message,
                 tag = "new document",
            )
            message.send()

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
    
class Download(models.Model):
    jobdocument = models.ForeignKey(to=JobDocument)
    downloaduser = models.ForeignKey(to=DownloadUser)
    
class LegacyImages(models.Model):
    image_name = models.CharField(max_length=100)
    caption = models.CharField(max_length=300)
    image_date = models.DateField()
    jobid = models.FloatField()
    inserted = models.BooleanField()