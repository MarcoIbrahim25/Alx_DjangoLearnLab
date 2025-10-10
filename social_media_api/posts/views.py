from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class StandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        obj, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            try:
                from notifications.utils import create_notification
                create_notification(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    target=post
                )
            except Exception:
                pass
            return Response({'detail': 'Liked', 'likes_count': post.likes.count()}, status=200)
        return Response({'detail': 'Already liked', 'likes_count': post.likes.count()}, status=200)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'detail': 'Unliked', 'likes_count': post.likes.count()}, status=200)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        try:
            from notifications.utils import create_notification
            create_notification(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )
        except Exception:
            pass

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
