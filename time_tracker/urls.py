from django.urls import path
from .views import ProjectCreateView, ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, CustomLoginView, RegisterView
from .views import TaskCategoryCreateView, TaskCategoryUpdateView, TaskCategoryDeleteView
from .views import TaskReportCreateView, UserTaskReportListView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('categories/create/<int:project_id>/', TaskCategoryCreateView.as_view(), name='taskcategory-create'),
    path('categories/<int:pk>/update/', TaskCategoryUpdateView.as_view(), name='taskcategory-update'),
    path('categories/<int:pk>/delete/', TaskCategoryDeleteView.as_view(), name='taskcategory-delete'),
    path('taskreports/create/<int:project_id>/', TaskReportCreateView.as_view(), name='taskreport-create'),
    path('my_taskreports/', UserTaskReportListView.as_view(), name='user-taskreport-list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
