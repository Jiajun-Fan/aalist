# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect 
from django.contrib import auth
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test 
from django.http import HttpResponse
from fantuan.models import MyGroup
from mail import sendSignUpMail
import aaforms

def signup(request):
    if request.method == 'POST':
        form = aaforms.UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'], 
                                     email = form.cleaned_data['email'],
                                     password = form.cleaned_data['password'])
            user.save() 
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth.login(request, user)
            return redirect('/user/info')
        else:
            return render(request, "signup.html", {'form': form})
    else:
        form = aaforms.UserForm()
        return render(request, "signup.html", {'form': form})

def login(request):
    if request.method == 'POST':
        form = aaforms.LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "login.html", {'form': form})
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if not user == None:
            auth.login(request, user)
            orig = request.GET.get('next', None)
            sendSignUpMail(user.email, user.username)
            if orig and not orig == '/login' and not orig == "/":
                return redirect(orig)
            else:
                return redirect('/user/info')
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

@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users = User.objects.all()
    return render_to_response("users.html", {'users': users})

@login_required
def info(request):
    user = request.user
    groupusers = user.mygroupuser_set.all()
    allgroupsquery = MyGroup.objects.all()
    groups = []
    allgroups = []
    for g in allgroupsquery:
        allgroups.append(g)
    new = False 
    if len(groupusers) == 0:
        new = True
    else:
        for gu in groupusers: 
            group = gu.group
            if group in allgroups:
                allgroups.remove(group)
                groups.append(group)
    return render_to_response("userinfo.html", 
                             {'user': user, "new":new, 'groups': groups, 'allgroups':allgroups},) 

def hello(request):
    return HttpResponse("hello, world!")
