'''определяет схемы URL для Learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    #home page
    path('', views.index, name ='index'),
    #page with a list of all topics
    path('topics/', views.topics, name='topics'),
    #page with a list of all public topics
    path('public_topics/', views.public_topics, name='public_topics'),
    #page with information about one topic
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    #page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    #page for adding a new public topic
    path('new_public_topic/', views.new_public_topic, name='new_public_topic'),
    #page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #page for edit a entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #delete topic
    path('del_topic/<int:topic_id>/', views.del_topic, name='del_topic'),
    #delete entry
    path('del_entry/<int:entry_id>/', views.del_entry, name='del_entry'),
    ]
