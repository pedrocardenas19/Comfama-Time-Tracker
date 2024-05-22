
from django.contrib import admin
from .models import Project, TaskCategory, TaskReport

admin.site.register(Project)
admin.site.register(TaskCategory)
admin.site.register(TaskReport)
