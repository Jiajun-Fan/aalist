from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect 
from django.contrib import auth
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from aalist.models import * 
from django.core import exceptions
import aaforms

@login_required
def groups(request):
    groups = MyGroup.objects.all()
    return render_to_response("groups.html", {'groups': groups})

@login_required
def createGroup(request):
    if request.method == 'POST':
        form = aaforms.GroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            group = MyGroup(name = name) 
            group.save() 
            group.members.add(request.user)
            return redirect('/')
        else:
            return render(request, "createGroup.html", {'form': form})
    else:
        form = aaforms.GroupForm()
        return render(request, "createGroup.html", {'form': form})

@login_required
def joinGroup(request):
    try:
        id = request.GET.get("id")
        group = MyGroup.objects.get(id=id)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("This group doesn't exist!")
    try:
        group.members.get(user=request.user)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("You are already in this group")
    groupuser = MyGroupUser(group=group, user=request.user, credit=0, active=True)
    groupuser.save()
    group.mygroupuser_set.add(groupuser)
    user.mygroupuser_set.add(groupuser)
    return redirect('/user/info')

@login_required
def optGroup(request):
    try: 
        id = request.GET.get("id")
        group = MyGroup.objects.get(id=id)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("This group doesn't exist!")
    groupusers = group.mygroupuser_set.all()
    users = []
    for g in groupusers:
        users.append(g.user)
    return render_to_response("group.html", {'group': group, 'users': users})
