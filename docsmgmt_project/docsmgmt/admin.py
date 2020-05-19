from django.contrib import admin

from .models import User, UserProfile, UserDepartment, UserSection, Documents, DocumentSections, Accepted, Comments, RefDocumentType

# Register your models here.
class DocumentsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.upload_by = request.user.profile
        obj.save()

admin.site.register(UserDepartment)
admin.site.register(UserSection)
admin.site.register(UserProfile)
admin.site.register(Documents, DocumentsAdmin)
admin.site.register(Accepted)
admin.site.register(Comments)
admin.site.register(RefDocumentType)