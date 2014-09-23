from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.http.response import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from ga.jobs.models import Job, DownloadUser, JobDocument, Download
from ga.jobs.forms import LoginForm
import json
from django.views.decorators.csrf import csrf_exempt


#===============================================================================
# JOB DETAIL
#===============================================================================
def detail(request, job_id, job_slug):
    
    try:
        job = Job.objects.prefetch_related(
            'documents'
        ).select_related(
            'staff', 'department'
        ).get(pk=job_id)
    except Job.DoesNotExist:
        return HttpResponseRedirect('/')

    ## CLEAN UP THE URL WHEN IT IS WRONG
    if not job.slug == job_slug:
        return HttpResponseRedirect(
            reverse('job:detail', kwargs={'job_id':job.id, 'job_slug':job.slug})
        )
    
    ## REQUIRE A LOGIN FOR DOCUMENT DOWNLOADING
    login_form = None
    logged_in = False
    if job.documents.all():
        if request.session.get('download_user'):
            logged_in = True
        else:
            ## VALIDATE THE LOGIN
            if request.POST:
                login_form = LoginForm(data=request.POST)
                if login_form.is_valid():
                    login = login_form.save()
                    request.session['download_user'] = login.pk
                    return HttpResponseRedirect(
                        reverse('job:detail', kwargs={'job_id':job.id, 'job_slug':job.slug})
                    )
            else:
                login_form = LoginForm()
                
    context = {
        'nav_selected': 'services',
        'job': job,
        'job_images': job.images.all().order_by('date'),
        'login_form': login_form,
        'logged_in': logged_in,
    }
    return render_to_response(
        template_name = 'detail.html',
        dictionary = Context(context),
        context_instance = RequestContext(request),
    )



#===============================================================================
# LOG DOWNLOAD
#===============================================================================
@csrf_exempt
def log_download(request):
    document_id = request.GET.get('doc')
    response_data = {'result':'failure'}
    if document_id:
        try:
            jobdocument = JobDocument.objects.get(pk=document_id)
            download_user = DownloadUser.objects.get(pk=request.session.get('download_user'))
            Download.objects.get_or_create(jobdocument = jobdocument, downloaduser = download_user)
            response_data['result'] = 'success'
        except JobDocument.DoesNotExist:
            response_data['message'] = 'Invalid Document'
        except DownloadUser.DoesNotExist:
            response_data['message'] = 'Invalid User'

    return HttpResponse(json.dumps(response_data), content_type="application/json")
