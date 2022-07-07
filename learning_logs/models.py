from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    '''topic of interest to the user'''
    text = models.CharField(max_length=200) #topic name
    data_added = models.DateTimeField(auto_now_add=True) #assign a date
    #key to associate the topic with the user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #If true, then it's public.
    public = models.BooleanField(default=False)
    def __str__(self):
        '''returns a string representation of the model'''
        return self.text

class Entry(models.Model):
    '''topic entry'''
    #key to associate the entry with the topic
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField() #entry text
    data_added = models.DateTimeField(auto_now_add=True)
    #Key to associate the entry with the user. The key is required 
    #to be able to edit and delete only your posts in public topics
    user_for_public = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        '''for admin panel'''
        verbose_name_plural = 'entreis'

    def __str__(self):
        '''returns the first 50 letters'''
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else: return f'{self.text}'
