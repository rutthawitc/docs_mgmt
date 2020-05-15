from django.contrib import admin
from .models import User, UserProfile, UserDepartment, UserSection, Documents, DocumentSections, Accepted, Comments, RefDocumentType

# Register your models here.
admin.site.register(UserDepartment)
admin.site.register(UserSection)
admin.site.register(UserProfile)
admin.site.register(Documents)
admin.site.register(Accepted)
admin.site.register(Comments)
admin.site.register(RefDocumentType)