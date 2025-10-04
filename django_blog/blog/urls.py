from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    register, profile
)

urlpatterns = [
    path("", home, name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("post/new/", PostCreateView.as_view(), name="post-new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="auth/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]
