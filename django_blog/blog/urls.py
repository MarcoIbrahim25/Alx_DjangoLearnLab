from django.urls import path
from .views import (
    home,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    register,
    profile
)

urlpatterns = [
    path("", home, name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("post/new/", PostCreateView.as_view(), name="post-new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-new"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
]
