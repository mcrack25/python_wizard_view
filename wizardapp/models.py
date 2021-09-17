from django.db import models

class Person(models.Model):
    lname = models.CharField(max_length=150, verbose_name='Фамилия')
    fname = models.CharField(max_length=150, verbose_name='Имя')
    sname = models.CharField(max_length=150, blank=True, verbose_name='Отчеств')

    def __str__(self):
        return self.lname

    class Meta:
        verbose_name = 'посетитель'
        verbose_name_plural = 'посетители'

class Messages(models.Model):
    text = models.TextField(verbose_name='Сообщение')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Посетитель')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'