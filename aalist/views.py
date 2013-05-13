from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.models import User
import aaforms

def signUp(request):
    if request.method == 'POST':
        form = aaforms.UserForm(request.POST)
        if form.is_valid():
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save() 
            users = User.objects.all()
            return render_to_response("users.html", {'users': users})
        else:
            return render(request, "signUp.html", {'form': form})
    else:
        form = aaforms.UserForm()
        return render(request, "signUp.html", {'form': form})
