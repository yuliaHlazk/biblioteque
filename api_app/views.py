from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Author, Publisher, Book
from .serializers import AuthorSerializer, PublisherSerializer, BookSerializer
import logging

logger = logging.getLogger(__name__)


class AuthorListCreate(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            logger.warning(f"unauthorized attempt to add author by {request.user}")
            return Response({"detail": "only admin can add authors"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"author '{serializer.data['name']}' created {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"author creation failed {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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
            logger.info(f"author '{author.name}' updated {request.user}")
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        author = self.get_object(pk)
        if not author:
            return Response({"detail": "Author not found"}, status=404)

        author_name = author.name
        author.delete()
        logger.info(f"author '{author_name}' deleted {request.user}")
        return Response({"message": "Author deleted successfully"}, status=200)


class BookListCreate(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "only admin can add books"}, status=403)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"book '{serializer.data['title']}' created {request.user}")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class BookDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            logger.warning(f"book with id {pk} not found")
            return None

    def get(self, request, pk):
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Book not found"}, status=404)

        if not request.user.is_authenticated:
            return Response({"detail": "authentication required"}, status=401)

        serializer = BookSerializer(book)
        
        logger.info(f"book '{book.title}' viewed {request.user.username}")
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        
        if not book:
            return Response({"detail": "Book not found"}, status=404)

        if not request.user.is_staff:
            return Response({"detail": "only admin can edit books"}, status=403)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"book '{book.title}' updated by admin {request.user.username}")
            return Response(serializer.data)
        logger.warning(f"book update failed for '{book.title}': {serializer.errors}")
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        book = self.get_object(pk)
        
        if not book:
            return Response({"detail": "Book not found"}, status=404)

        if not request.user.is_staff:
            logger.warning(f"user {request.user.username} tried to delete book '{book.title}' without permissions")
            return Response({"detail": "Only admin can delete books"}, status=403)

        logger.info(f"book '{book.title}' deleted by admin {request.user.username}")
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=200)
