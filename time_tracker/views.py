from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, TaskCategory, TaskReport
from .forms import ProjectForm,  TaskCategoryForm, TaskReportForm
from .mixins import StaffRequiredMixin
from django.core.exceptions import PermissionDenied


class RegisterView(View):
    form_class = UserCreationForm
    template_name = 'time_tracker/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project-list')
        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    template_name = 'time_tracker/login.html'



class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'time_tracker/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)
    
class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'time_tracker/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user not in self.object.members.all() and not self.request.user.is_staff:
            raise PermissionDenied
        context['categories'] = TaskCategory.objects.filter(project=self.object)
        context['category_form'] = TaskCategoryForm(initial={'project': self.object})
        context['reports'] = TaskReport.objects.filter(category__project=self.object)
        context['report_form'] = TaskReportForm()
        return context

    
class ProjectCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'time_tracker/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'time_tracker/project_form.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Project
    template_name = 'time_tracker/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')


class TaskCategoryCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = TaskCategory
    form_class = TaskCategoryForm

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.project.get_absolute_url()

class TaskCategoryUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = TaskCategory
    form_class = TaskCategoryForm

    def get_success_url(self):
        return self.object.project.get_absolute_url()

class TaskCategoryDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = TaskCategory

    def get_success_url(self):
        return self.object.project.get_absolute_url()
    
class TaskReportCreateView(LoginRequiredMixin, CreateView):
    model = TaskReport
    form_class = TaskReportForm
    template_name = 'time_tracker/taskreport_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_id'])
        if request.user not in self.project.members.all() and not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        context['categories'] = TaskCategory.objects.filter(project=self.project)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        category_id = self.request.POST.get('category')
        form.instance.category = get_object_or_404(TaskCategory, pk=category_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project-detail', kwargs={'pk': self.project.id})


class UserTaskReportListView(LoginRequiredMixin, ListView):
    model = TaskReport
    template_name = 'time_tracker/user_taskreport_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return TaskReport.objects.filter(user=self.request.user).order_by('-date')
    
from .utils import generate_pie_chart

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'time_tracker/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user not in self.object.members.all() and not self.request.user.is_staff:
            raise PermissionDenied
        context['categories'] = TaskCategory.objects.filter(project=self.object)
        context['category_form'] = TaskCategoryForm(initial={'project': self.object})
        context['reports'] = TaskReport.objects.filter(category__project=self.object)
        context['report_form'] = TaskReportForm()
        context['pie_chart'] = generate_pie_chart(self.object)
        return context