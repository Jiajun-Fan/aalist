# -*- coding: utf-8 -*- 
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
import string
import random

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
            item = {'name': g.user.username, 'credit': float(g.credit)/100, 'uid':g.id}
            users.append(item)
        formset = OptFormSet(initial=users)
        return render(request, "group.html", {'group': group, 'formset': formset})
    else:
        OptFormSet = formset_factory(aaforms.OptionForm)
        formset = OptFormSet(request.POST)
        if formset.is_valid():
            try: 
                gid = request.POST.get("gid")
                group = MyGroup.objects.get(id=gid)
            except exceptions.ObjectDoesNotExist:
                return HttpResponse("This group doesn't exist!")
            total = 0
            cnt = 0
            divcnt = 0
            owntotal = 0
            for form in formset:
                if form.cleaned_data["select"] == True:
                    cnt = cnt + 1
                    paid = int(string.atof(form.cleaned_data["paid"])*100)
                    own = int(string.atof(form.cleaned_data["own"])*100)
                    if paid > 0:
                        total = total + paid 
                    if own > 0:
                        owntotal = owntotal + own
                    else:
                        divcnt = divcnt + 1
            if total < owntotal: 
                return HttpResponse(u"总付款金额小于总应付金额")
            m1 = total - owntotal
            badluck = {} 
            if m1:
                if divcnt == 0:
                    return HttpResponse(u"总付款金额与总应付金额不一致")
                else:
                    reminder = m1 % divcnt
                    m1 = m1 - reminder
                    badluck = getRandomList(divcnt-1, reminder)
            activity = MyActivity(cost=total, group=group)
            activity.save()
            ret = "total: {}\n".format(total)
            i = 0
            for form in formset:
                if form.cleaned_data["select"] == True:
                    paid = int(string.atof(form.cleaned_data["paid"])*100)
                    own = int(string.atof(form.cleaned_data["own"])*100)
                    if own > 0:
                        ret = ret + "paid: {}, own: {}, final: {}\n".format(paid, own, paid-own)
                    else:
                        own = m1 / divcnt
                        if badluck.has_key(i):
                            own = own + 1
                        i = i + 1
                        ret = ret + "paid: {}, own: {}, final: {}\n".format(paid, own, paid-own)
                    delta = paid - own
                    try:
                        uid = form.cleaned_data["uid"]
                        groupuser = group.mygroupuser_set.get(id=uid)
                    except exceptions.ObjectDoesNotExist:
                        return HttpResponse("uid error")
                    groupuser.credit = groupuser.credit + delta
                    groupuser.save()
                    record = MyRecord(value=delta, groupuser=groupuser, activity=activity)
                    groupuser.myrecord_set.add(record)
                    activity.myrecord_set.add(record)
                    record.save()
            return HttpResponse(ret)
        else:
            return render(request, "group.html", {'formset': formset})

def getRandomList(a, b):
    ret = {}
    while not b == 0:
        c = random.randint(0, a)
        if not ret.has_key(c):
            b = b - 1
            ret[c] = c
    return ret
