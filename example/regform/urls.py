from django.urls import path
from .views import all_users, loginpage, welcome, zaglushka, current_post, UserPostCreateView, UserPostDeleteView, RegisteredUserCreateView, RegisteredUserUpdateView, happynew, one_user_posts, show_user, happyold
urlpatterns = [
    path('', welcome, name='welcome'),
    path('loginpage/', loginpage, name='loginpage'),
    path('add/', RegisteredUserCreateView.as_view(), name = 'add'),
    path('update/<int:pk>/', RegisteredUserUpdateView.as_view(), name = 'update'),
    path('newsuccess/', happynew, name='happynew'),
    path('oldsuccess/', happyold, name='happyold'),
    path('zaglushka/', zaglushka, name='zaglushka'),
    path('all_users/', all_users, name='all_users'),
    path('user/<int:registered_user_id>/', show_user, name='show_user'),
    path('user/<int:registered_user_id>/posts/', one_user_posts, name='one_user_posts'),
    path('user/<int:pk>/addpost/', UserPostCreateView.as_view(), name='addpost'),
    path('user/<int:pk>/bye_post/<int:post_id>', UserPostDeleteView.as_view(), name='deletepost'),
    path('user/<int:registered_user_id>/post/<int:post_id>/', current_post, name='current_post'),
    #path('', index, name='index'),
]
