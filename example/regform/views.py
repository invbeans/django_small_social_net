from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import RegisteredUserForm, UserPostForm
from .models import RegisteredUser, UserPost
from django.urls import reverse_lazy, reverse

def happynew(request):
    return HttpResponse("Пользователь успешно добавлен")

def happyold(request):
    return HttpResponse("Пользователь успешно отредактирован")

def zaglushka(request):
    return HttpResponse("Пост успешно добавлен")

def welcome(request):
    return render(request, 'regform/welcome.html')

def all_users(request, **kwargs):
    user_id = 0
    def get_user_id(self, **kwargs):
        user_id = self.kwargs['pk']
    all_registered_users = RegisteredUser.objects.all()
    context = {'all_registered_users': all_registered_users, 'user_id': user_id}
    return render(request, 'regform/all_users.html', context)

def loginpage(request):
    login = request.POST.get('login')
    password = request.POST.get('password')
    current_registered_user = RegisteredUser.objects.get(pk=1)
    request.session['user_id'] = 0
    try:
        current_registered_user = RegisteredUser.objects.get(login=login)
        registered_user_id = current_registered_user.pk
        request.session['user_login'] = current_registered_user.login
        request.session['user_name'] = current_registered_user.name
        request.session['user_surname'] = current_registered_user.surname
        request.session['user_fathers_name'] = current_registered_user.fathers_name
        request.session['user_age'] = current_registered_user.age
        request.session['user_email'] = current_registered_user.email
        request.session['user_id'] = registered_user_id
        #context = {'current_registered_user': current_registered_user, 'registered_user_id': registered_user_id}
        return redirect('show_user', registered_user_id)
    except current_registered_user.DoesNotExist:
        print('oops')
    return render(request, 'regform/loginpage.html')


def show_user(request, registered_user_id):
    user_id = request.session['user_id']
    #def get_user_id(self, **kwargs):
     #   user_id = self.kwargs['pk']
    current_registered_user = RegisteredUser.objects.get(pk=registered_user_id)
    context = {'current_registered_user': current_registered_user, 'registered_user_id': registered_user_id}
    if(user_id == registered_user_id):
        return render(request, 'regform/userpage.html', context)
    else:
        return render(request, 'regform/otheruserpage.html', context)

def one_user_posts(request, registered_user_id):
    user_id = request.session['user_id']
    current_user_posts = UserPost.objects.filter(user__id = registered_user_id)
    current_registered_user = RegisteredUser.objects.get(pk=registered_user_id)
    context = {'current_user_posts': current_user_posts, 'current_registered_user': current_registered_user, 'registered_user_id': registered_user_id}
    if(registered_user_id == user_id):
        return render(request, 'regform/userposts.html', context)
    else:
        return render(request, 'regform/otheruserposts.html', context)

def current_post(request, registered_user_id, post_id):
    user_id = request.session['user_id']
    current_post = UserPost.objects.get(pk=post_id)
    current_registered_user = RegisteredUser.objects.get(pk=registered_user_id)
    context = {'current_post': current_post, 'current_registered_user': current_registered_user}
    if(current_registered_user.id == user_id):
        return render(request, 'regform/onepost.html', context)
    else:
        return render(request, 'regform/otheronepost.html', context)

class RegisteredUserCreateView(CreateView):
    template_name = 'regform/create.html'
    form_class = RegisteredUserForm
    success_url = reverse_lazy('happynew')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registered_users'] = RegisteredUser.objects.all()
        return context

class UserPostCreateView(CreateView):
    template_name = 'regform/addpost.html'
    user_id = 0
    form_class = UserPostForm
    success_url = reverse_lazy('zaglushka')
    def get_user_id(self, **kwargs):
        user_id = self.kwargs['pk']
    def get_success_url(self):
        return reverse('one_user_posts', args=[self.user.id])
    def get_context_data(self, **kwargs):
        self.user = get_object_or_404(RegisteredUser, id=self.kwargs['pk'])
        kwargs['user'] = self.user
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.user = get_object_or_404(RegisteredUser, id=self.kwargs['pk'])
        form.instance.user = self.user
        return super().form_valid(form)

class UserPostDeleteView(DeleteView):
    template_name='regform/deletepost.html'
    form_class = UserPostForm
    #success_url = reverse_lazy(happynew)
    def get_object(self):
        userpost = get_object_or_404(UserPost, id = self.kwargs['post_id'])
        return userpost
    def get_success_url(self):
        return reverse('one_user_posts', args=[self.kwargs['pk']])


class RegisteredUserUpdateView(UpdateView):
    template_name= 'regform/update.html'
    model = RegisteredUser
    success_url = reverse_lazy('happyold')
    fields = ('login', 'password', 'name', 'surname', 'fathers_name', 'age', 'email')
    def get_object(self):
        current_registered_user = get_object_or_404(RegisteredUser, id = self.request.session['user_id'])
        self.request.session['user_login'] = current_registered_user.login
        self.request.session['user_name'] = current_registered_user.name
        self.request.session['user_surname'] = current_registered_user.surname
        self.request.session['user_fathers_name'] = current_registered_user.fathers_name
        self.request.session['user_age'] = current_registered_user.age
        self.request.session['user_email'] = current_registered_user.email
        return current_registered_user
    
