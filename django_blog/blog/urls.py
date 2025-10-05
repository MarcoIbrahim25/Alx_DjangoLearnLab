from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    register, profile,
    comment_create, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path("", home, name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("post/new/", PostCreateView.as_view(), name="post-new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    path("post/<int:post_id>/comments/new/", comment_create, name="comment-new"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),

    path("login/", LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]
