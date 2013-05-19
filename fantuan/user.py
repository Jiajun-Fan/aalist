from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect 
from django.contrib import auth
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from fantuan.models import MyGroup
import aaforms

def signup(request):
    if request.method == 'POST':
        form = aaforms.UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'], 
                                     email = form.cleaned_data['email'],
                                     password = form.cleaned_data['password'])
            user.save() 
            return redirect('/')
        else:
            return render(request, "signup.html", {'form': form})
    else:
        form = aaforms.UserForm()
        return render(request, "signup.html", {'form': form})

def login(request):
    if request.method == 'POST':
        form = aaforms.LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse("illegal input")
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if not user == None:
            auth.login(request, user)
            orig = request.GET.get('next', None)
            if orig and not orig == '/login':
                return redirect(orig)
            else:
                return redirect('/')
        else:
            form = aaforms.LoginForm()
            return render(request, "login.html", {'form': form})
    else:
        orig = request.GET.get('next', None)
        if not orig:
            orig = "/"
        form = aaforms.LoginForm()
        return render(request, "login.html", {'form': form, 'from': orig})

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def users(request):
    users = User.objects.all()
    return render_to_response("users.html", {'users': users})

@login_required
def info(request):
    user = request.user
    groupusers = user.mygroupuser_set.all()
    groups = []
    for u in groupusers:
        groups.append(u.group)
    return render_to_response("userinfo.html", 
                             {'user': user, 'groups': groups},) 

def hello(request):
    return HttpResponse("hello, world!")
