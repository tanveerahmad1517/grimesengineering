from django.shortcuts import render_to_response, render
from django.template.context import Context, RequestContext
from django.http.response import HttpResponseRedirect
from ga.jobs.models import Client
from django.views.generic.base import TemplateView
from ga.forms import ContactForm


#===============================================================================
# HOME PAGE
#===============================================================================
# @cache_page(60 * 15)
def index(request):
    context = {
        'nav_selected': 'home',
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
            new_contact = form.save()

            ## SEND AN EMAIL TO THE MEMBERSHIP DIRECTOR rwchamp1
#             postmark_email('SMC - New Member Signup', 'rwchamp1@gmail.com', new_member.full_info(cr='\n'), 'new member')
            context['success'] = True

        return render(request, self.template_name, context)
    
    def get(self, request):
        context = {
           'nav_selected': 'contact',
           'contact_form': ContactForm(),
           'template_name': self.template_name,
        }
        return render(request, self.template_name, context)