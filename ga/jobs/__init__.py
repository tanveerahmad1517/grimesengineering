from ga.jobs.models import JobDocument
def context_processor(request):
    return {
        'AVAILABLE_DOCUMENTS': JobDocument.objects.available_documents(),
    }