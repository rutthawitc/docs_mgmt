from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

# Create your models here.
class Roles(models.Model):
    role_code = models.CharField(max_length=20)
    role_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.role_code

class UserDepartment(models.Model):
    department_code = models.CharField(max_length=35)
    department_title = models.CharField(max_length=150)
    department_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class UserSection(models.Model):
    section_code = models.CharField(max_length=35)
    section_title = models.CharField(max_length=150)
    section_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.section_title

class DocumentTemplates(models.Model):
    DEFAULT_PK = 1
    template_code = models.CharField(max_length=10)
    template_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.template_desc

class RefDocumentType(models.Model):
    type_code = models.CharField(max_length=10)
    type_desc = models.CharField(max_length=150)

    def __str__(self):
        return self.type_desc

class Documents(models.Model):
    template_code = models.ForeignKey(DocumentTemplates, default=DocumentTemplates.DEFAULT_PK)
    type_code = models.ForeignKey(RefDocumentType, on_delete=models.CASCADE)
    access_count = models.IntegerField()
    doc_mtno = models.CharField(max_length=50)
    doc_title = models.CharField(max_length=150)
    doc_desc = models.CharField(max_length=150)
    doc_date = models.DateField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.doc_title

class DocumentSections(models.Model):
    doc_no = models.ForeignKey(DocumentSections, on_delete=models.CASCADE)
    section_title = models.CharField(max_length=100)
    section_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.section_title

class RoleDocumentAccessRight(models.Model):
    role_code = models.ForeignKey(Roles, on_delete=models.CASCADE)
    doc_no = models.ForeignKey(Documents, on_delete=models.CASCADE)

#User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, null=True, blank=True)
    read_role = models.ForeignKey(ReadRole, on_delete=models.SET_NULL, null=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    sect = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
#This will create a userprofile each time a user is saved if it is created. You can then use
#user.get_profile().whatever    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)

#Store a additional Note for Document
class Comment(models.Model):
    doc = models.ForeignKey(Documents, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    comment_date =models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.doc.doc_title
