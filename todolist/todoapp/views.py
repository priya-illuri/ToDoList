from django.shortcuts import render

# Create your views here.
from django.views import *
from django.db.models import *
from django.views.generic import *
from .models import *
from django.shortcuts import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("login")



class UserTasksListView(ListView):
    model=User
    template_name = 'task_list.html'
    def get_object(self, queryset=None):
        return get_object_or_404(MyTasks,**self.kwargs)
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(UserTasksListView,self).get_context_data(**kwargs)
        usr=self.request.user
        #context['cards']=self.model.objects.all().values()
        context['allusers']=usr.mytasks_set.values('id','category','task_name','task_desc','currentdate','duedate')
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

from django import forms

from todoapp.models import MyTasks

class AddTask(forms.ModelForm):
    class Meta:
        model = MyTasks
        exclude=['id','user','currentdate']
        widgets={
            'category' : forms.TextInput(attrs={'class':'form-control','placeholder':'enter category'}),
            'task_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name of task'}),
            'task_desc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ur task'}),
            #'created_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'expiry date'}),
            'duedate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'due date'}),
        }

class CreateTaskView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    permission_required = "creditcard:add_mytask"
    permission_denied_message = "user doesnot have permission to add college"
    raise_exception = True
    template_name = 'task_form.html'
    model=MyTasks
    form_class=AddTask
    def post(self, request, *args, **kwargs):
        user=request.user
        task_form=AddTask(request.POST)
        # import ipdb
        # ipdb.set_trace()
        if task_form.is_valid():
            task=task_form.save(commit=False)
            task.user=user
            import datetime
            now = datetime.datetime.now()
            task.currentdate=now.strftime("%Y-%m-%d")
            # import ipdb
            # ipdb.set_trace()
            task.save()
        return redirect('tasks_html')
    #success_url = reverse_lazy('creditcard:cards_html')


class UpdateTaskView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    def has_permission(self):
        if self.request.user.id==MyTasks.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
            return True
        else:
            return False
    # def has_permission(self):
    #     if self.request.user.id==self.kwargs['id']:
    #         return True
    #     else:
    #         return False
        # user=self.request.user
        # id=self.kwargs['userid']
    #if user.id==CreditCard.objects.filter(id=self.kwargs['id'].values('userid')[0]['userid'])
    login_url = '/login/'
    # permission_required = "creditcard:change_mytask"
    # permission_denied_message = "user doesnot have permission to change college"
    # raise_exception = True
    template_name = 'task_form.html'
    #permission_required = 'onlineapp.add_college'
    #permission_denied_message='user doesnot have permission to create college'
    model=MyTasks
    form_class=AddTask

    def get_object(self, queryset=None):
        return get_object_or_404(MyTasks,**self.kwargs)

    success_url = reverse_lazy('tasks_html')


class DeleteTaskView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    def has_permission(self):
        if self.request.user.id==MyTasks.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
            return True
        else:
            return False
    login_url = 'login/'
    permission_required = "mytasks:delete_mytasks"
    permission_denied_message = "user doesnot have permission to delete college"
    raise_exception = True
    template_name = 'delete.html'
    #permission_required = 'onlineapp.add_college'
    #permission_denied_message='user doesnot have permission to create college'
    model=MyTasks

    success_url = reverse_lazy('tasks_html')
    def get_object(self, queryset=None):
        return get_object_or_404(MyTasks,**self.kwargs)


class ViewByCategory(LoginRequiredMixin,ListView):
    # def has_permission(self):
    #     if self.request.user.id==MyTasks.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
    #         return True
    #     else:
    #         return False
    login_url = 'login/'
    model=MyTasks
    template_name='category.html'
    def get_object(self, queryset=None):
        return get_object_or_404(MyTasks,**self.kwargs)
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(ViewByCategory,self).get_context_data(**kwargs)
        usr=self.request.user
        #context['cards']=self.model.objects.all().values()
        context['allcategories']=usr.mytasks_set.values('category').annotate(dcount=Count('category'))

        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context

class ViewCategoryTasks(LoginRequiredMixin,ListView):
    # def has_permission(self):
    #     if self.request.user.id==MyTasks.objects.filter(id=self.kwargs['id']).values('user_id')[0]['user_id']:
    #         return True
    #     else:
    #         return False
    login_url = 'login/'
    model=MyTasks
    template_name='category_detail.html'
    def get_object(self, queryset=None):
        return get_object_or_404(MyTasks,**self.kwargs)
    def get_context_data(self,**kwargs):
        # if not self.request.user.is_authenticated():
        #     redirect("onlineapp:login")
        context=super(ViewCategoryTasks,self).get_context_data(**kwargs)
        usr=self.request.user
        #context['cards']=self.model.objects.all().values()
        context['allusers']=usr.mytasks_set.filter(category=self.kwargs['category']).values()
        # import ipdb
        # ipdb.set_trace()
        context.update({'user_permissions':self.request.user.get_all_permissions()})
        return context
