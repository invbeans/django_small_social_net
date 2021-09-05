from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, DateTimeField
from django.urls import reverse
from django.core import validators
from datetime import datetime
from django.shortcuts import get_object_or_404

# Create your models here.
class RegisteredUser(models.Model):
    def __str__(self):
        return self.name

    login = models.CharField(
        max_length=40, unique=True, verbose_name="Логин", blank=True
    )
    password = models.CharField(
        max_length=40, verbose_name="Пароль", default="Придумайте надежный пароль"
    )
    name = models.CharField(max_length=30, verbose_name="Имя", blank=True)
    surname = models.CharField(max_length=30, verbose_name="Фамилия", blank=True)
    fathers_name = models.CharField(max_length=30, verbose_name="Отчество", blank=True)
    age = models.SmallIntegerField(verbose_name="Возраст", blank=True)
    email = models.EmailField(verbose_name="Почта", blank=True)
    problematic = models.BooleanField(
        verbose_name="Нарушения", default=False, editable=False
    )
    custom_url = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name="Пользовательский url (по желанию)",
        blank=True,
        null=True,
        validators=[
            validators.RegexValidator(
                regex="^(?=.*[a-zA-Z])",
                message="Пользовательский url обязан иметь хотя бы одну букву",
            )
        ],
    )


# validate_slug
class UserPost(models.Model):
    def get_absolute_url(self):
        return reverse("current_post", args=[str(self.user__id), str(self.pk)])

    title = models.CharField(
        max_length=40, verbose_name="Заголовок поста", default="Заголовок"
    )
    content = models.TextField(verbose_name="Содержимое", blank=True)
    datetime = DateTimeField(
        auto_now=True, verbose_name="Дата изменения", editable=False
    )
    amount_likes = models.SmallIntegerField(
        verbose_name="Лайки", editable=False, default=0
    )
    user = models.ForeignKey(
        RegisteredUser, on_delete=CASCADE, verbose_name="Автор", editable=False
    )

    class Meta:
        verbose_name = "Пост пользователя"
        verbose_name_plural = "Посты пользователя"
        ordering = ["-datetime"]


class PostReact(models.Model):
    from_post = models.ForeignKey(
        UserPost, on_delete=CASCADE, verbose_name="Пост с реакциями", null=True
    )
    react_type = models.SmallIntegerField(
        blank=True, null=True, verbose_name="Лайк - 0, коммент - 1"
    )
    react_time = models.DateTimeField(
        auto_now=True, verbose_name="Время появления реакции"
    )
    reacted_user_id = models.SmallIntegerField(
        blank=True, null=True, verbose_name="Юзер который реагирует"
    )

    def need_to_delete(self):
        if (datetime.now() - self.react_time).days > 30:
            return True
        else:
            return False

    # im not sure if it will work properly :(
    # def delete(self):
    #   if self.need_to_delete():
    #      super().delete()

    def like_count(self, post_id, user_id):
        record = PostReact.objects.filter(
            from_post=UserPost.objects.get(id=post_id),
            reacted_user_id=user_id,
            react_type=0,
        )
        if record.exists():
            self.from_post.amount_likes = self.from_post.amount_likes - 1
            record.delete()
        else:
            record = PostReact(
                from_post=UserPost.objects.get(id=post_id),
                react_type=0,
                react_time=datetime.now(),
                reacted_user_id=user_id,
            )
            record.save()
            self.from_post.amount_likes = self.from_post.amount_likes + 1

        # if record:
        #   self.from_post.amount_likes = self.from_post.amount_likes - 1
        #  record.delete()
        # else:
        #   record.create()
        #  self.from_post.amount_likes = self.from_post.amount_likes + 1
        return self.from_post.amount_likes
