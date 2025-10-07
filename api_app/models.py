from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    CHOICES = [
        ("novel", "Novel"),
        ("drama", "Drama"),
        ("poetry", "Poetry"),
        ("fantasy", "Fantasy"),
        ("nonfiction", "Non-Fiction"),
        ("other", "Other"),
    ]
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.PROTECT, related_name="books"
    )

    title = models.CharField(max_length=250)
    genre = models.CharField(max_length=30, choices=CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
