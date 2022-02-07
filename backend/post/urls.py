from django.urls import path
from .views import LoginView, RegisterView, UserView, LogoutView, FileUploadView, ListPost

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('upload', FileUploadView.as_view()),
    path('posts', ListPost.as_view(), name='list_posts')
]
