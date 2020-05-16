from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

# Create your models here.
class UserDepartment(models.Model):
    DEFAULT_PK=3
    department_code = models.CharField(max_length=35)
    department_title = models.CharField(max_length=150)
    department_desc = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.department_title

class UserSection(models.Model):
    department_code = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)
    section_code = models.CharField(max_length=35)
    section_title = models.CharField(max_length=150)
    section_desc = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.section_title

class RefDocumentType(models.Model):
    type_code = models.CharField(max_length=10)
    type_desc = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.type_desc

class Documents(models.Model):
    type_code = models.ForeignKey(RefDocumentType, on_delete=models.CASCADE)
    access_count = models.IntegerField(null=True, blank=True)
    doc_mtno = models.CharField(max_length=50,blank=True, null=True)
    doc_title = models.CharField(max_length=150)
    doc_desc = models.CharField(max_length=150, blank=True, null=True)
    doc_date = models.DateField(auto_now=False, null=True, blank=True)
    doc_dept = models.ForeignKey(UserDepartment, on_delete=models.CASCADE, default=UserDepartment.DEFAULT_PK)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doc_title

class DocumentSections(models.Model):
    doc_no = models.ForeignKey(Documents, on_delete=models.CASCADE)
    section_title = models.CharField(max_length=100)
    section_sequence = models.IntegerField()
    section_desc = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.section_title

#User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, null=True, blank=True)
    employee_id = models.CharField(max_length=12)
    dept = models.ForeignKey(UserDepartment, on_delete=models.SET_NULL, null=True, blank=True)
    sect = models.ForeignKey(UserSection, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
#This will create a userprofile each time a user is saved if it is created. You can then use
#user.get_profile().whatever    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)

#Store a additional note for Document
class Comments(models.Model):
    doc_no = models.ForeignKey(Documents, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    comment_date =models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.doc_no.doc_title

class Accepted(models.Model):
    doc_no = models.ForeignKey(Documents, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.doc_no.doc_title


