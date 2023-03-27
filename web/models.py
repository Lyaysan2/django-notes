import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название тега')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Note(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.CharField(max_length=256, verbose_name='Текст')
    created_at = models.DateTimeField(verbose_name='Дата создания')
    updated_at = models.DateTimeField(verbose_name='Дата последнего редактирования')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    image = models.ImageField(upload_to='notes/', null=True, blank=True, verbose_name='Картинка')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'заметка'
        verbose_name_plural = 'заметки'