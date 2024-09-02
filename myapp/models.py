from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Login_table(AbstractUser):

    usertype=models.CharField(max_length=25)

class Add_leader(models.Model):

    name=models.CharField(max_length=25,null=True)
    team_name=models.CharField(max_length=25,null=True)
    job_name=models.CharField(max_length=25,null=True)
    employee_id=models.CharField(max_length=25,null=True)
    contact=models.CharField(max_length=25,null=True)
    email=models.EmailField(null=True)
    profile_picture=models.ImageField(null=True)
    login_id=models.ForeignKey(Login_table,on_delete=models.CASCADE,null=True)

class Add_member(models.Model):

    name=models.CharField(max_length=25,null=True)
    job_name=models.CharField(max_length=25,null=True)
    employee_id=models.CharField(max_length=25,null=True)
    contact=models.CharField(max_length=25,null=True)
    email=models.EmailField(null=True)
    profile_picture=models.ImageField(null=True)
    leader_id=models.ForeignKey(Add_leader,on_delete=models.CASCADE,null=True)
    login_id=models.ForeignKey(Login_table,on_delete=models.CASCADE,null=True)

class Add_project(models.Model):
    title = models.CharField(max_length=50, null=True)
    project_image = models.ImageField(null=True)
    description = models.CharField(max_length=500, null=True)
    submission_date = models.DateTimeField(null=True)
    uploaded_date = models.DateTimeField(null=True)
    leader_id = models.ForeignKey(Add_leader, on_delete=models.CASCADE, null=True)
    first_member_id = models.ForeignKey(Add_member, on_delete=models.CASCADE, null=True, related_name='projects_first_member')
    second_member_id = models.ForeignKey(Add_member, on_delete=models.CASCADE, null=True, related_name='projects_second_member')
    third_member_id = models.ForeignKey(Add_member, on_delete=models.CASCADE, null=True, related_name='projects_third_member')
    fourth_member_id = models.ForeignKey(Add_member, on_delete=models.CASCADE, null=True, related_name='projects_fourth_member')
    fifth_member_id = models.ForeignKey(Add_member, on_delete=models.CASCADE, null=True, related_name='projects_fifth_member')
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    leader_approvel = models.BooleanField(default=False)
    leader_rejected = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    assigned = models.BooleanField(default=False)
    
class Add_comment(models.Model):

    comment=models.CharField(max_length=250,null=True)
    sent_by=models.DateTimeField(null=True)
    member_id=models.ForeignKey(Add_member,on_delete=models.CASCADE,null=True)
    project_id=models.ForeignKey(Add_project,on_delete=models.CASCADE,null=True)

