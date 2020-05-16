from django.urls import path, include
from .views import Home, ShowAllDocuments, ShowDocsByDept

urlpatterns = [
    path('', Home, name='home'),
    path('showall/', ShowAllDocuments, name='showalldocs'),
    path('showbydept/', ShowDocsByDept, name='showbydept'),
]
