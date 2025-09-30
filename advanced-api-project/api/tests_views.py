from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.author = Author.objects.create(name="George Orwell")
        self.book = Book.objects.create(title="1984", publication_year=1949, author=self.author)

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("1984", str(response.data))

    def test_detail_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")

    def test_create_book_requires_authentication(self):
        url = reverse("book-create")
        data = {"title": "Animal Farm", "publication_year": 1945, "author": self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="testuser", password="password123")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("book-update", kwargs={"pk": self.book.pk})
        data = {"title": "Nineteen Eighty-Four", "publication_year": 1949, "author": self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Nineteen Eighty-Four")

    def test_delete_book(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_filter_books_by_year(self):
        url = reverse("book-list") + "?publication_year=1949"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        url = reverse("book-list") + "?search=1984"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("1984", str(response.data))

    def test_order_books_by_title(self):
        Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author)
        url = reverse("book-list") + "?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))
