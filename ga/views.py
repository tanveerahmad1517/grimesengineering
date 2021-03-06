from django.shortcuts import render_to_response, render
from django.template.context import Context, RequestContext
from django.http.response import HttpResponseRedirect
from ga.jobs.models import Client, Job
from django.views.generic.base import TemplateView
from ga.forms import ContactForm
from ga.services.models import Department
from django.contrib import messages
from ga.functions import postmark_email


#===============================================================================
# HOME PAGE
#===============================================================================
# @cache_page(60 * 15)
def index(request):
    
    recent_jobs = Job.objects.select_related('images').filter(
        is_featured=True,
    ).order_by('-date')[:4]
    
    departments = Department.objects.filter(
        name__in = ['Environmental','Architecture & Engineering',]
    ).order_by('name')[:3]
    
    context = {
        'nav_selected': 'home',
        'recent_jobs': recent_jobs,
        'departments': departments,
    }
    return render_to_response(
        template_name = 'index.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )

#===============================================================================
# CLIENT LIST
#===============================================================================
def clientlist(request):
    try:
        clients = Client.objects.all()
    except Client.DoesNotExist:
        return HttpResponseRedirect('/')
    
    context = {
        'nav_selected': 'clients',
        'clients': clients,
        'description': 'Grimes & Associates has served thousands of clients in our 30 year history.'
    }
    return render_to_response(
        template_name = 'clientlist.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )
    
#===============================================================================
# MEMBERSHIP
#===============================================================================
class Contact(TemplateView):
    template_name = 'contact.html'
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        context = {
            'nav_selected': 'contact',
            'contact_form': form,
            'template_name': self.template_name,
        }
        
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            msg = form.cleaned_data['message']
            message = 'Name: %s\nEmail: %s\nMessage:\n%s' % (name, email, msg)
            postmark_email('Message from G&A website', 'grimes@grimesengineering.com', message, 'contact_email')
            messages.success(request, 'Your message has been sent')

        return render(request, self.template_name, context)
    
    def get(self, request):
        context = {
           'nav_selected': 'contact',
           'contact_form': ContactForm(),
           'template_name': self.template_name,
        }
        return render(request, self.template_name, context)