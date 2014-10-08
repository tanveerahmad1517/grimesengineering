from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from ga.about.models import Staff, License


#===============================================================================
# ABOUT MAIN
#===============================================================================
def index(request):
    context = {
        'nav_selected': 'about',
    }
    return render_to_response(
        template_name = 'about.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )
    
#===============================================================================
# ABOUT TEAM
#===============================================================================
def team(request):
    context = {
        'nav_selected': 'about',
        'staff': Staff.objects.select_related('department').filter(active=True).order_by('department__sort', 'sort')
    }
    return render_to_response(
        template_name = 'team.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )
#===============================================================================
# ABOUT LICENSES
#===============================================================================
def licenses(request):
    licenses = License.objects.prefetch_related('staff').select_related('category', 'name').all().order_by('category__name', 'staff__sort')
    context = {
        'nav_selected': 'about',
        'licenses': licenses
    }
    return render_to_response(
        template_name = 'licenses.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )