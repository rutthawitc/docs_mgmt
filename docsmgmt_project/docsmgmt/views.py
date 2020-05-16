from django.shortcuts import render
from .models import Documents, UserProfile, UserDepartment
import json
from django.http import JsonResponse

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

def UpdateAccepted(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    print('Document Id:', documentId)
    print('Action:', action)

    #Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    #accepted = DocAccepted.objects.create(user=user, docs=document)
    #accepted.save()

    print('User:', user)
    print('Document ID:', document)

    return JsonResponse('Accepted', safe=False)

