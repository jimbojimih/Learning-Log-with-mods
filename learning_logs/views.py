from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404

def index(request):
    '''home page'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''personal topics with the filter'''
    topics = Topic.objects.filter(owner=request.user).exclude(public=True).order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def public_topics(request):
    '''public topics with the filter'''
    topics = Topic.objects.filter(public=True).order_by('data_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/public_topics.html', context)

def topic(request, topic_id):
    '''one topic with entreis'''
    topic = Topic.objects.get(id=topic_id)
    #if the topic is not public, then we compare the creator
    #of the topic and the user sending the request
    if topic.public == False:  
        chek_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-data_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''create a new topic'''
    if request.method != 'POST':
        #create a form
        form = TopicForm()
    else:
        #processing the completed form
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            #create user attribute
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            return redirect('learning_logs:topics')
        #output form
    context = {'form' : form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_public_topic(request):
    '''create a new public topic'''
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data = request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.public = True
            topic.save()
            form.save()
            return redirect('learning_logs:public_topics')
    context = {'form' : form}
    return render(request, 'learning_logs/new_public_topic.html', context)

@login_required        
def new_entry(request, topic_id):
    '''create a new entry'''
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            if topic.public == False: 
                chek_topic_owner(topic, request)
            #create an attribute needed to check for edit
            #and delet of your entry in someone else's
            #public topic
            new_entry.user_for_public = request.user
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    #checking edit and delete your entry
    check_entry_user(entry, request)
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry' : entry, 'topic' : topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)

def del_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    chek_topic_owner(topic, request)
    topic.delete()
    return render(request, 'learning_logs/index.html')

def del_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    check_entry_user(entry, request)
    entry.delete()
    return render(request, 'learning_logs/index.html')

def chek_topic_owner(topic, request):
    '''check that the topic belongs to the current user'''
    if topic.owner != request.user:
        raise Http404

def check_entry_user(entry, request):
    '''check that the entry belongs to the current user'''
    if entry.user_for_public != request.user:
        raise Http404   
