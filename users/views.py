from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    """регистрируем нового пользователя"""
    if request.method != 'POST':
        #выводим пустую форму
        form = UserCreationForm()
    else:
        #обработка заполненной формы
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #выполнение входа и перенаправ. на дом страницу
            login(request, new_user)
            return redirect('learning_logs:index')
    #вывести пустую или недействительную форму
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

def del_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
        #logout(request)
        user.delete()
        return redirect('learning_logs:index')
    else: raise Http404
