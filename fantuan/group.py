from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect 
from django.contrib import auth
from django.contrib.auth import authenticate 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.http import HttpResponse
from fantuan.models import * 
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
            groupuser = MyGroupUser(group=group, user=request.user, credit=0, active=True)
            groupuser.save()
            group.mygroupuser_set.add(groupuser)
            request.user.mygroupuser_set.add(groupuser)
            return redirect('/')
        else:
            return render(request, "createGroup.html", {'form': form})
    else:
        form = aaforms.GroupForm()
        return render(request, "createGroup.html", {'form': form})

@login_required
def joinGroup(request):
    try:
        gid = request.GET.get("gid")
        group = MyGroup.objects.get(id=gid)
    except exceptions.ObjectDoesNotExist:
        return HttpResponse("This group doesn't exist!")
    groupusers = group.mygroupuser_set.filter(user__id=request.user.id)
    if not len(groupusers) == 0: 
        return HttpResponse("You are already in this group")
    else:
        groupuser = MyGroupUser(group=group, user=request.user, credit=0, active=True)
        groupuser.save()
        group.mygroupuser_set.add(groupuser)
        request.user.mygroupuser_set.add(groupuser)
        return redirect('/user/info')

@login_required
def optGroup(request):
    if request.method == 'GET':
        try: 
            gid = request.GET.get("gid")
            group = MyGroup.objects.get(id=gid)
        except exceptions.ObjectDoesNotExist:
            return HttpResponse("This group doesn't exist!")
        groupuser = group.mygroupuser_set.filter(user__id=request.user.id)
        if len(groupuser) == 0: 
            return HttpResponse("You are not member of this group!")
        groupusers = group.mygroupuser_set.all()
        users = []
        OptFormSet = formset_factory(aaforms.OptionForm, extra=0)
        for g in groupusers:
            item = {'name': g.user.username, 'credit': g.credit}
            users.append(item)
        formset = OptFormSet(initial=users)
        return render(request, "group.html", {'group': group, 'users': users, 'formset': formset})
    else:
        return HttpResponse("TODO")
