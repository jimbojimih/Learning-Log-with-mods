from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    """register a new user"""
    if request.method != 'POST':
        #create a form
        form = UserCreationForm()
    else:
        #processing the completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')
    #output form
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

def del_user(request, user_id):
    """delete a user"""
    user = User.objects.get(id=user_id)
    #this code is needed to delete only the current account
    if request.user == user: 
        user.delete()
        return redirect('learning_logs:index')
    else: raise Http404
