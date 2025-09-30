from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Book.objects.all().order_by('-publication_year')
        title = self.request.query_params.get('title')
        year = self.request.query_params.get('year')
        if title:
            qs = qs.filter(title__icontains=title)
        if year:
            qs = qs.filter(publication_year=year)
        return qs

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
