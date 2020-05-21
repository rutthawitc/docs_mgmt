from django.urls import path, include
from .views import Home, ShowAllDocuments, ShowDocsByDept, DocAccepted, DocDetail, ShowUnreadDocs, ShowAcceptedDocs, loginuser, logoutuser, getcomment

urlpatterns = [
    path('', Home, name='home'),
    path('showall/', ShowAllDocuments, name='showalldocs'),
    path('showbydept/', ShowDocsByDept, name='showbydept'),
    path('accepted/', DocAccepted, name='accepted'),
    path('docdetail/<int:doc_pk>', DocDetail, name='docdetail'),
    path('unread/', ShowUnreadDocs, name='unread'),
    path('showaccepted/', ShowAcceptedDocs, name='showaccepted'),
    path('login/', loginuser, name='loginuser'),
    path('logout/', logoutuser, name='logoutuser'),
    path('getcomment/', getcomment, name='getcomment')
]

