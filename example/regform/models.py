from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, DateTimeField
from django.urls import reverse
from django.core import validators
import datetime

# Create your models here.
class RegisteredUser(models.Model):
    def __str__(self):
        return self.name
    login = models.CharField(max_length=40, unique=True, verbose_name='Логин', blank = True)
    password = models.CharField(max_length=40, verbose_name='Пароль', default='Придумайте надежный пароль')
    name = models.CharField(max_length=30, verbose_name='Имя', blank = True)
    surname = models.CharField(max_length=30, verbose_name='Фамилия', blank = True)
    fathers_name = models.CharField(max_length=30, verbose_name='Отчество', blank = True)
    age = models.SmallIntegerField(verbose_name='Возраст', blank = True)
    email = models.EmailField(verbose_name='Почта', blank = True)
    problematic = models.BooleanField(verbose_name='Нарушения', default = False, editable = False)
    custom_url = models.SlugField(max_length=30, unique=True, verbose_name='Пользовательский url (по желанию)', blank=True, null=True, validators=[validators.RegexValidator(regex="^(?=.*[a-zA-Z])", message="Пользовательский url обязан иметь хотя бы одну букву")])

#validate_slug
class UserPost(models.Model):
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('current_post', args=[str(self.user__id), str(self.pk)])

    title = models.CharField(max_length=40, verbose_name='Заголовок поста', default='Заголовок')
    content = models.TextField(verbose_name='Содержимое', blank=True)
    datetime = DateTimeField(auto_now=True, verbose_name='Дата изменения', editable=False)
    amount_likes = models.SmallIntegerField(verbose_name='Лайки', editable=False, default=0)
    user = models.ForeignKey(RegisteredUser, on_delete=CASCADE, verbose_name='Автор', editable=False)

    class Meta:
        verbose_name='Пост пользователя'
        verbose_name_plural='Посты пользователя'
        ordering = ['-datetime']

class PostReact(models.Model):
    def __str__(self):
        return self.name

    def need_to_delete(self):
        if((datetime.now() - self.react_time).days > 30):
            return True
        else:
            return False

    #im not sure if it will work properly :(
    def delete(self):
        if self.need_to_delete():
            super().delete()

    def like_count(self):
        record, created = PostReact.objects.get_or_create(from_post__user__id = self.from_post__user__id, react_type = 0)
        if(created == False):
            self.from_post__amount_likes = self.from_post__amount_likes - 1
            record.delete()
        else:
            self.from_post__amount_likes = self.from_post__amount_likes + 1


    from_post = models.ForeignKey(UserPost, on_delete=CASCADE, verbose_name="Пост с реакциями")
    react_type = models.SmallIntegerField(blank=True, null=True, verbose_name="Лайк - 0, коммент - 1")
    react_time = models.DateTimeField(auto_now=True, verbose_name="Время появления реакции")
