from django.db import models
from ga import settings

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit
from ga.services.models import Department

class LicenseCategory(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "License Categories"

    def __unicode__(self):
        return self.name

class LicenseName(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name

class License(models.Model):
    name = models.ForeignKey(to=LicenseName)
    number = models.CharField(max_length=100)
    category = models.ForeignKey(to=LicenseCategory)
    
    def __unicode__(self):
        return '%s; %s' % (self.name.name, self.number)

class Staff(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True,)
    title = models.CharField(max_length=500, null=True, blank=True,)
    license = models.ManyToManyField(License, null=True, blank=True,)
    description = models.TextField(null=True, blank=True,)
    phone = models.CharField(max_length=100, null=True, blank=True,)
    cell = models.CharField(max_length=100, null=True, blank=True,)
    department = models.ForeignKey(to=Department, null=True, blank=True,)
    active = models.BooleanField(default=True)
    sort = models.IntegerField(default=10, null=True,)
    image = models.ImageField(null=True, blank=True, upload_to = settings.MEDIA_ROOT)
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFit(250, 250)],
        format='JPEG',
        options={'quality': 60},
    )
    
    class Meta:
        verbose_name_plural = "Staff"
        
    def __unicode__(self):
        return self.name