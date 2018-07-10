"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todoapp.views import *
from todoapp.auth import *
app_name='todoapp'


urlpatterns = [
    path("logout/",logout_view,name='logout'),
    path('admin/', admin.site.urls),
    path('tasks/',UserTasksListView.as_view(),name='tasks_html'),
    path('tasks/category/',ViewByCategory.as_view(),name='category_html'),
    path('tasks/category/<category>/',ViewCategoryTasks.as_view(),name='category_detail_html'),
    path('tasks/update/<int:id>',UpdateTaskView.as_view(),name='update_html'),
    path('tasks/delete/<int:id>',DeleteTaskView.as_view(),name='delete_html'),
    path('tasks/add/',CreateTaskView.as_view(),name='add_tasks_html'),
    path("login/",LoginController.as_view(),name='login'),
]

