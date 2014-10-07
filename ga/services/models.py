from django.db import models
from django.template.defaultfilters import slugify

from tinymce.models import HTMLField
from django.core.urlresolvers import reverse

class DepartmentManager(models.Manager):
    #===========================================================================
    # CREATE A TREE OF CATEGORIES AND SUBCATEGORIES FOR USE IN THE NAVIGATION
    #===========================================================================
    def tree(self):
        tree = []
        for parent in self.filter(parent_id__isnull=True, navigation_display=True).order_by('sort').values():
            parent['leaves'] = self.filter(parent_id=parent['id'], navigation_display=True).order_by('sort').values()
            tree.append(parent)
        return tree

class Department(models.Model):
    name = models.CharField(max_length=100)
    parent_id = models.ForeignKey('self', null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    navigation_display = models.BooleanField(default=False)
    sort = models.IntegerField()
    
    objects = DepartmentManager()
    
    def __unicode__(self):
        return self.name
    
    @property
    def icon(self):
        if self.name.lower() == 'environmental':
            return 'leaf'
        if self.name.lower() == 'engineering':
            return 'cogs'
        if self.name.lower() == 'architecture':
            return 'university'
        return None
    
    @property
    def slug(self):
        return slugify(self.name)
    
    @property
    def url(self):
        return reverse(
            'services:department', 
            kwargs = {
                'department_id': self.id, 
                'department_slug': self.slug,
            }
        )