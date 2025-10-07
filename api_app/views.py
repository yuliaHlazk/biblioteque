from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author, Publisher, Book
from .serializers import AuthorSerializer, PublisherSerializer, BookSerializer


class AuthorListCreate(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None

    def get(self, request, pk):
        author = self.get_object(pk)
        if not author:
            return Response({"detail": "Author not found"}, status=404)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = self.get_object(pk)
        if not author:
            return Response({"detail": "Author not found"}, status=404)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        author = self.get_object(pk)
        if not author:
            return Response({"detail": "Author not found"}, status=404)
        author.delete()
        return Response({"message": "Author deleted successfully"}, status=200)


class BookListCreate(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    def get(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Book not found"}, status=404)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Book not found"}, status=404)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Book not found"}, status=404)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=200)
