from django.db import models

class Person(models.Model):
    lname = models.CharField(max_length=150, verbose_name='Фамилия')
    fname = models.CharField(max_length=150, verbose_name='Имя')
    sname = models.CharField(max_length=150, blank=True, verbose_name='Отчеств')

class Messages(models.Model):
    text = models.TextField(verbose_name='Сообщение')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Посетитель')
