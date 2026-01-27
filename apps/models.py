from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey, SET_NULL, CASCADE


# Create your models here.
class User(AbstractUser):
    pass


class Project(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=ForeignKey('apps.User',on_delete=SET_NULL,related_name='projects',null=True,blank=True)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()


class Sprint(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField()
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    project=ForeignKey('apps.Project',on_delete=CASCADE,related_name='sprints')
    created_at=models.DateTimeField(auto_now_add=True)



class Task(models.Model):
    class StatusChoices(models.TextChoices):
        new='new','New'
        in_progress='in_progress','In Progress'
        done='done',"Done"
    class PriorityChoices(models.TextChoices):
        low='low','Low'
        medium='medim','Medim'
        high='high','High'
    name=models.CharField(max_length=255)
    description=models.TextField()
    status=models.CharField(max_length=255,choices=StatusChoices.choices,default=StatusChoices.new)
    priority=models.CharField(max_length=255,choices=PriorityChoices.choices)
    user=ForeignKey('apps.User',on_delete=CASCADE,related_name='tasks') #worker
    # created_by=ForeignKey('apps.User',on_delete=CASCADE,related_name='my_tasks')
    sprint=ForeignKey('apps.Sprint',on_delete=CASCADE,related_name='tasks')
    created_at=models.DateTimeField(auto_now_add=True)




class AssignHistory(models.Model):
    reason=models.CharField(max_length=500)
    task=ForeignKey('apps.Task',on_delete=SET_NULL,related_name='history',null=True,blank=True)
    old_worker=ForeignKey('apps.User',on_delete=SET_NULL,null=True,blank=True,related_name='old_worker')
    new_worker=ForeignKey('apps.User',on_delete=SET_NULL,null=True,blank=True,related_name='new_worker')
    created_at=models.DateTimeField(auto_now_add=True)




