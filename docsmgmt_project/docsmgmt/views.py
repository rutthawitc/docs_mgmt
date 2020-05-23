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
#Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    #print(context)
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
    
    #Filter unread from readed_docsQuerySet
    unread_list = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    ).exclude(id__in=readed_docs).order_by('-id')
    docscount = unread_list.count()

    #Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(unread_list, 15)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error ="ไม่มีเอกสารใหม่"
    context = {'error':error, 'docs':docs, 'docscount':docscount }
    return render(request, 'docsmgmt/unread.html', context)

@login_required
#Show Accepted Documents filter by User ID! 
def ShowAcceptedDocs(request):
    #Find Readed - QuerySet
    accepted_list = Accepted.objects.filter(
        Q(is_accepted=True) &
        Q(user__user_id=request.user.profile.id)
    ).order_by('-accepted_date')
    acceptedcount = accepted_list.count()
    #Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(accepted_list, 15)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error ={"No data!"}
    context = {'error':error, 'docs':docs, 'acceptedcount':acceptedcount }
    return render(request, 'docsmgmt/showaccepted.html', context)

@login_required
def ShowDocsByDept(request):
    #Complete -QuerySet-
    docs_list = Documents.objects.filter(
        Q(doc_dept=request.user.profile.dept) |
        Q(doc_dept__id=3)
    ).order_by('-doc_dept__id')
    docscount = docs_list.count()
    #Paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(docs_list, 15)
    #-----DEBUG-------
    #print(paginator.count)
    #print(paginator.num_pages)
    #print(paginator.page_range)
    try:
        docs = paginator.page(page)
    except PageNotAnInteger:
        docs = paginator.page(1)
    except EmptyPage:
        docs = paginator.page(paginator.num_pages)

    error ={"No data!"}
    context = {'docs':docs, 'error':error, 'docscount':docscount}
    return render(request, 'docsmgmt/docsbydept.html', context)

@login_required
def DocAccepted(request):
    data = json.loads(request.body)
    documentId = data['documentId']
    action = data['action']
    #--DEBUG---
    #print('Document Id:', documentId)
    #print('Action:', action)

    #Set values
    user = request.user.profile
    document = Documents.objects.get(id=documentId)

    accepted = Accepted.objects.create(user=user, doc_no=document, is_accepted=True)
    accepted.save()
    #--DEBUG---
    #print('User:', user)
    #print('Document ID:', document)

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
    #--DEBUG---
    #print('Document Id:', documentId)
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






    



