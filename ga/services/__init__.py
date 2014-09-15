from ga.services.models import Department
def context_processor(request):
    return {
        'DEPARTMENT_TREE': Department.objects.tree(),
    }