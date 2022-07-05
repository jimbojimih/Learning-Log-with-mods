from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404

def index(request):
    '''домагная страница приложения Learning Log'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''выводим список тем'''
    topics = Topic.objects.filter(owner=request.user).exclude(public=True).order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def public_topics(request):
    '''выводим список общих тем'''
    topics = Topic.objects.filter(public=True).order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/public_topics.html', context)

@login_required
def topic(request, topic_id):
    '''одна тема и её записи'''
    topic = Topic.objects.get(id=topic_id)
    if topic.public == False: #если тема не общая, то 
        chek_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-data_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''определяет новую тему'''
    if request.method != 'POST':
        #данные не отправлялись, создаётся пустая форма
        form = TopicForm()
    else:
        #Отправлены данные POST, обработать данные
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return redirect('learning_logs:topics')
        #вывести пустую или недействительную форму.
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_public_topic(request):
    '''определяет новую общую тему'''
    if request.method != 'POST':
        #данные не отправлялись, создаётся пустая форма
        form = TopicForm()
    else:
        #Отправлены данные POST, обработать данные
        form = TopicForm(data = request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.public = True
            topic.save()
            form.save()
            return redirect('learning_logs:public_topics')
        #вывести пустую или недействительную форму.
    context = {'form' : form}
    return render(request, 'learning_logs/new_public_topic.html', context)

@login_required        
def new_entry(request, topic_id):
    '''определяет новую запись по теме'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        #данные не отправлялись, создаётся пустая форма
        form = EntryForm()
    else:
        #Отправлены данные POST, обработать данные
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            if topic.public == False: #если тема не общая, то
                chek_topic_owner(topic, request)
            else: new_entry.user_for_public = request.user
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    #вывести пустую или недействительную форму.
    context = {'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''редактирует существующую запись'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if f'{entry.user_for_public}' != f'{request.user}': #если тема не общая, то 
        raise Http404
        #print(entry.user_for_public)
        #print(request.user)
        
    if request.method != 'POST':
        #исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)
    else:
        #Отправка данных POST, обработать данные
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    #вывести пустую или недействительную форму.
    context = {'entry' : entry, 'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required        
def del_topic(request, topic_id):
    '''определяет новую запись по теме'''
    topic = Topic.objects.get(id=topic_id)
    chek_topic_owner(topic, request)
    topic.delete()
    return render(request, 'learning_logs/index.html')

@login_required        
def del_entry(request, entry_id):
    '''определяет новую запись по теме'''
    #topic = Topic.objects.get(id=topic_id)
    entry = Entry.objects.get(id=entry_id)
    #chek_topic_owner(topic, request)
    entry.delete()
    return render(request, 'learning_logs/index.html')

def chek_topic_owner(topic, request):
    '''проверяем, что тема принадлежить текущему пользователю'''
    if topic.owner != request.user:
        raise Http404
        
