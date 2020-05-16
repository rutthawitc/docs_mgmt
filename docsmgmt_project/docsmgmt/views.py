from django.shortcuts import render
from .models import Documents, UserProfile, UserDepartment

# Create your views here.
def Home(request):
    context = {}
    return render(request, 'docsmgmt/home.html', context)

def ShowAllDocuments(request):
    docs = Documents.objects.all()
    error ={"No data!"}
    context = {'docs':docs, 'error':error}
    return render(request, 'docsmgmt/alldocs.html', context)

def ShowDocsByDept(request):
    docs_dept = Documents.objects.filter(doc_dept=request.user.profile.dept)
    all_docs = Documents.objects.filter(doc_dept__id=3)

    error ={"No data!"}
    context = {'all_docs':all_docs, 'docs_dept':docs_dept, 'error':error}
    return render(request, 'docsmgmt/docsbydept.html', context)

