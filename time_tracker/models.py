
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    required_hours = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})


class TaskCategory(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='task_categories')

    def __str__(self):
        return self.name



class TaskReport(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='task_reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_spent = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.title
