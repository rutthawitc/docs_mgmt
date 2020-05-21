from django.shortcuts import render, redirect, get_object_or_404
from .models import Documents, UserProfile, UserDepartment, Accepted, Comments
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q
import json
from django.views.generic import ListView, CreateView, UpdateView
#from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@login_required
def Home(request):
    #show document counter on home page.
    #readed
    readed_docs = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    ).values_list('doc_no',flat=True)

    readed_count = readed_docs.count()

    #unread
    unread_docs = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    ).exclude(id__in=readed_docs)

    unread_count = unread_docs.count()

    context = {'unread_count':unread_count, 'readed_count':readed_count}
    print(context)
    return render(request, 'docsmgmt/home.html', context)

@login_required
def ShowAllDocuments(request):
    docs = Documents.objects.all()
    error ="ไม่มีเอกสารใหม่"
    context = {'docs':docs, 'error':error}
    return render(request, 'docsmgmt/alldocs.html', context)

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def DocDetail(request, doc_pk):
    doc = Documents.objects.get(id=doc_pk)
    comments = Comments.objects.filter(doc_no=doc.id)
    try:
        isaccepted = Accepted.objects.get(doc_no=doc.id, user=request.user.id)
    except Accepted.DoesNotExist:
        isaccepted = None

    context = {'doc':doc, 'isaccepted':isaccepted, 'comments':comments}
    return render(request, 'docsmgmt/docdetail.html', context)

def getcomment(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    text = data['memo']
    print('Document Id:', documentId)
    #print('Action:', action)
    #print('text:', text)

    #Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    print(user)
    print('Doc ID :',document.id)
    print('text:', text)
    comment = Comments.objects.create(user=user, doc_no=document, comment=text)
    comment.save()

    return JsonResponse('Commented', safe=False)

def loginuser(request):
    username_value = ''
    password_vlaue = ''
    if request.method == 'GET':
        return render(request, 'docsmgmt/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        print(request.POST['username'])
        print(request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'docsmgmt/login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
           login(request, user)
           return redirect('home')


@login_required
def logoutuser(request):
    #if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect('/login/')

#class DocumentView(CreateView):
#    model = Documents
#    fields = ('type_code', 'doc_mtno', 'doc_title', 'doc_desc', 'doc_date', 'doc_dept', 'doc_file')
#    success_url = reverse_lazy('home')






    



