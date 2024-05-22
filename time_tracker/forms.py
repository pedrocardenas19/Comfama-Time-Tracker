from django import forms
from django.contrib.auth.models import User
from .models import Project, TaskCategory, TaskReport

class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = ['name', 'members', 'required_hours', 'start_date', 'end_date']

class TaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['name', 'project']
        widgets = {'project': forms.HiddenInput()}

class TaskReportForm(forms.ModelForm):
    class Meta:
        model = TaskReport
        fields = ['title', 'time_spent', 'date']