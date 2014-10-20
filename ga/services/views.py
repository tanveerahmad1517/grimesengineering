from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from ga.services.models import Department
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ga.jobs.models import Job


#===============================================================================
# HOME PAGE
#===============================================================================
def services(request, department_id, department_slug):
    try:
        department = Department.objects.get(pk=department_id)
        jobs = Job.objects.select_related('images').filter(
            status__name='Completed', 
            display=True, 
            department=department
        ).order_by('date')
    except Department.DoesNotExist:
        return HttpResponseRedirect('/')
    
    for item in jobs:
        print item
    
    
    if not department.slug == department_slug:
        return HttpResponseRedirect(
            reverse('services:department', kwargs={'department_id':department.id, 'department_slug':department.slug}))
    context = {
        'nav_selected': 'services',
        'department': department,
        'jobs': jobs,
    }
    return render_to_response(
        template_name = 'services.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )
