from django.forms import ModelForm
from .models import RegisteredUser, UserPost


class RegisteredUserForm(ModelForm):
    class Meta:
        model = RegisteredUser
        fields = (
            "login",
            "password",
            "name",
            "surname",
            "fathers_name",
            "age",
            "email",
        )


class UserPostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ("title", "content")

class UploadAvatarForm(ModelForm):
    class Meta:
        model = RegisteredUser
        fields = ('image',)
