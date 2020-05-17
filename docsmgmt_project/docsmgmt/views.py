from django.shortcuts import render
from .models import Documents, UserProfile, UserDepartment, Accepted
import json
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def Home(request):
    context = {}
    return render(request, 'docsmgmt/home.html', context)

def ShowAllDocuments(request):
    docs = Documents.objects.all()
    error ="ไม่มีเอกสารใหม่"
    context = {'docs':docs, 'error':error}
    return render(request, 'docsmgmt/alldocs.html', context)

#Show Unreaded Documents filter by Current User ID! 
def ShowUnreadDocs(request):
    #Find Readed (Accepted Documents) - QuerySet
    readed_docs = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    ).values_list('doc_no',flat=True)
    
    #Filter Unread (UnAccepted) from Readed Resualt
    #Filter by userID
    #unread_docs = Documents.objects.exclude(id__in=readed_docs)

    #Test
    unread_docs = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    ).exclude(id__in=readed_docs)

    error ="ไม่มีเอกสารใหม่"
    context = {'error':error, 'unread_docs':unread_docs }
    return render(request, 'docsmgmt/unread.html', context)

#Show Accepted Documents filter by User ID! 
def ShowAcceptedDocs(request):
    #Find Readed - QuerySet
    readed_docs = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    )

    error ={"No data!"}
    context = {'error':error, 'readed_docs':readed_docs }
    return render(request, 'docsmgmt/showaccepted.html', context)


def ShowDocsByDept(request):
    #Original filter
    #docs_dept = Documents.objects.filter(doc_dept=request.user.profile.dept)
    #all_docs = Documents.objects.filter(doc_dept__id=3)

    #Complete -QuerySet
    docs_dept = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    )

    error ={"No data!"}
    context = {'docs_dept':docs_dept, 'error':error}
    return render(request, 'docsmgmt/docsbydept.html', context)

def DocAccepted(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    print('Document Id:', documentId)
    print('Action:', action)

    #Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    accepted = Accepted.objects.create(user=user, doc_no=document, is_accepted=True)
    accepted.save()

    print('User:', user)
    print('Document ID:', document)

    return JsonResponse('Accepted', safe=False)

def DocDetail(request, doc_pk):
    doc = Documents.objects.get(id=doc_pk)

    context = {'doc':doc}
    return render(request, 'docsmgmt/docdetail.html', context)

