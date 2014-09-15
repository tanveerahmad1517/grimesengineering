from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from ga.about.models import Staff


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
        'staff': Staff.objects.select_related('department').filter(active=True).order_by('department')
    }
    return render_to_response(
        template_name = 'team.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )