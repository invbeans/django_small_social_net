from django.urls import path
from .views import all_users, loginpage, welcome, zaglushka, current_post, UserPostCreateView, UserPostDeleteView, RegisteredUserCreateView, RegisteredUserUpdateView, happynew, one_user_posts, show_user, happyold
urlpatterns = [
    path('', welcome, name='welcome'),
    path('loginpage/', loginpage, name='loginpage'),
    path('add/', RegisteredUserCreateView.as_view(), name = 'add'),

    path('update/<int:param>/', RegisteredUserUpdateView.as_view(), name = 'update'),
    path('update/<slug:param>/', RegisteredUserUpdateView.as_view(), name = 'update'),

    path('newsuccess/', happynew, name='happynew'),
    path('oldsuccess/', happyold, name='happyold'),
    path('zaglushka/', zaglushka, name='zaglushka'),
    path('all_users/', all_users, name='all_users'),

    path('user/<int:param>/', show_user, name='show_user'),
    path('user/<slug:param>/', show_user, name = 'show_user'),

    path('user/<int:param>/posts/', one_user_posts, name='one_user_posts'),
    path('user/<slug:param>/posts/', one_user_posts, name='one_user_posts'),

    path('user/<int:param>/addpost/', UserPostCreateView.as_view(), name='addpost'),
    path('user/<slug:param>/addpost/', UserPostCreateView.as_view(), name='addpost'),

    path('user/<int:param>/bye_post/<int:post_id>', UserPostDeleteView.as_view(), name='deletepost'),
    path('user/<slug:param>/bye_post/<int:post_id>', UserPostDeleteView.as_view(), name='deletepost'),

    path('user/<int:param>/post/<int:post_id>/', current_post, name='current_post'),
    path('user/<slug:param>/post/<int:post_id>/', current_post, name='current_post'),
    #path('', index, name='index'),
]
