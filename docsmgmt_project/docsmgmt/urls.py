from django.urls import path, include
from .views import Home, ShowAllDocuments

urlpatterns = [
    path('', Home, name='home'),
    path('showall/', ShowAllDocuments, name='showalldocs'),
]
