from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyTasks(models.Model):
    category = models.CharField(max_length=128) #attributes
    task_name = models.CharField(max_length=64)
    task_desc = models.CharField(max_length=250)
    duedate=models.DateField()
    currentdate = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name