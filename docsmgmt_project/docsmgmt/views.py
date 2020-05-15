from django.shortcuts import render
from .models import Documents

# Create your views here.
def Home(request):
    context = {}
    return render(request, 'docsmgmt/home.html', context)

def ShowAllDocuments(request):
    docs = Documents.objects.all()
    error ={"No data!"}
    context = {'docs':docs, 'error':error}
    return render(request, 'docsmgmt/alldocs.html', context)
