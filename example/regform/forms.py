from django.forms import ModelForm
from .models import RegisteredUser, UserPost

class RegisteredUserForm(ModelForm):
    class Meta:
        model = RegisteredUser
        fields = ('login', 'password', 'name', 'surname', 'fathers_name', 'age', 'email')

class UserPostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ('title', 'content')

#login = models.CharField(max_length=40, unique=True, verbose_name='Логин'),
    # name = models.CharField(max_length=30, verbose_name='Имя'),
    # surname = models.CharField(max_length=30, verbose_name='Фамилия'),
    # fathers_name = models.CharField(max_length=30, verbose_name='Отчество', blank = True),
    # age = models.SmallIntegerField(verbose_name='Возраст'),
    # email = models.EmailField(),
    # problematic = models.BooleanField(default = False, editable = False),