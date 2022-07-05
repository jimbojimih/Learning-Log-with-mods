from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    '''Тема, которую изучает пользователь'''
    text = models.CharField(max_length=200) #атрибут для хранения текста
    data_added = models.DateTimeField(auto_now_add=True) #присвоить тек.дату
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    def __str__(self):
        '''возвращает строковое представление модели.'''
        return self.text

class Entry(models.Model):
    '''Информация, изученная пользователем по теме'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)#присвоить ключ, связь с топиком
    text = models.TextField() #атрибут для хранения текста
    data_added = models.DateTimeField(auto_now_add=True) #присвоить тек.дату
    #user_for_public = models.TextField(default='') #сохраняем имя создателя записи в общих темах
    user_for_public = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        '''дополнительная информация по управл.моделью, форма множ.числа Entr'''
        verbose_name_plural = 'entreis'

    def __str__(self):
        '''возвращает строковое представление модели.'''
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else: return f'{self.text}'
