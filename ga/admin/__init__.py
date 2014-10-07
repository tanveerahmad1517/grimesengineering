from django.contrib import admin

from django.contrib.auth.models import Group
admin.site.unregister(Group)

class StaffAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(StaffAdmin, self).queryset(request)
        return qs.filter(active=True).order_by('sort')
from ga.about.models import Staff
admin.site.register(Staff, StaffAdmin)

class LicenseNameAdmin(admin.ModelAdmin):
    pass
from ga.about.models import LicenseName
admin.site.register(LicenseName, LicenseNameAdmin)

class LicenseAdmin(admin.ModelAdmin):
    pass
from ga.about.models import License
admin.site.register(License, LicenseAdmin)

class LicenseCategoryAdmin(admin.ModelAdmin):
    pass
from ga.about.models import LicenseCategory
admin.site.register(LicenseCategory, LicenseCategoryAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    pass
from ga.services.models import Department
admin.site.register(Department, DepartmentAdmin)

from ga.jobs.models import JobDocument
class JobDocumentInline(admin.TabularInline):
    model = JobDocument
    extra = 0

from ga.jobs.models import JobImage
class JobImageInline(admin.TabularInline):
    model = JobImage
    extra = 0

class JobAdmin(admin.ModelAdmin):
    inlines = (JobImageInline, JobDocumentInline,)
from ga.jobs.models import Job
admin.site.register(Job, JobAdmin)

class JobStatusAdmin(admin.ModelAdmin):
    pass
from ga.jobs.models import JobStatus
admin.site.register(JobStatus, JobStatusAdmin)

class ClientAdmin(admin.ModelAdmin):
    pass
from ga.jobs.models import Client
admin.site.register(Client, ClientAdmin)
