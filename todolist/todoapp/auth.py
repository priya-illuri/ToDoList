from django import forms
from django.views import View
from django.shortcuts import *
from django.contrib.auth import authenticate,login


# import sys,os,django
# sys.path.append("C:\PythonCourse\my\my")
# os.environ["DJANGO_SETTINGS_MODULE"]= "my.settings"
# django.setup()



class LoginForm(forms.Form):

    username=forms.CharField(
        max_length=75,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','place-holder':'username'})
    )

    password=forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control','place-holder':'password'})
    )





class LoginController(View):
    def get(self,request):
        form=LoginForm
        template_name='login.html'
        return render(request,template_name,{'form':form})

    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():


            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            if user is not None:
                login(request,user)
                return redirect("tasks_html")
            else:
                return redirect("login")
                # template_name = 'templates/signup.html'
                # return render(request, template_name, {'form': form})

        else:
            return redirect("login")
            #template_name='templates/signup.html'
            # return render(request, template_name, {'form': form})
