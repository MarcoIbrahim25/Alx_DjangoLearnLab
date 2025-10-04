from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.PostListView.as_view(), name="posts"),
    path("posts/new/", views.PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("login/", LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="auth/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
