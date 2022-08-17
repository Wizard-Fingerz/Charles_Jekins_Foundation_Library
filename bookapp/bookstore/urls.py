from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # shared urls
    path('', views.home, name= "home"),
    path('login_form/', views.login_form, name="login_form"),
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('regform/', views.register_form, name="regform"),
    path('register/', views.registerView, name="register"),
    path('emailform/', views.EmailForm.as_view(), name="emailform"),
    
    # publisher url
    path('library/', views.UBookListView.as_view(), name="library"),
    path('group_chat/', views.UCreateChat.as_view(), name=""),
    path('group_chat/', views.UListChat.as_view(), name="group_chat"),
    path('request_form/', views.request_form, name="request_form"),
    path('book_request/', views.book_request, name="book_request"),
    path('feedback_form/', views.feedback_form, name="feedback_form"),
    path('send_feedback/', views.send_feedback, name="send_feedback"),
    path('about/', views.about, name="about"),
    path('usearch/', views.usearch, name="usearch"),
    path('profile/', views.profile, name='profile'),

]