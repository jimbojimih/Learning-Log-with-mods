'''определяет схемы URL для Learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    #домашняя страница
    path('', views.index, name ='index'),
    #страница со списком всех тем.
    path('topics/', views.topics, name='topics'),
    #страница со списком всех общих тем.
    path('public_topics/', views.public_topics, name='public_topics'),
    #страница с информацией по одной теме
    path('topic/<int:topic_id>/', views.topic, name='topic'),
    #страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    #страница для добавления общей темы
    path('new_public_topic/', views.new_public_topic, name='new_public_topic'),
    #страница для добавления новой записи
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    #удалить топик
    path('del_topic/<int:topic_id>/', views.del_topic, name='del_topic'),
    path('del_entry/<int:entry_id>/', views.del_entry, name='del_entry'),
    ]
