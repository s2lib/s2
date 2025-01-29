from django.db import models

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Ensures each email is unique
    phone = models.CharField(max_length=10)  # Or use PhoneNumberField if needed
    address = models.TextField()
    doj = models.DateField(verbose_name="Date of Joining")
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default='active'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-doj']  # Orders students by the date of joining


class S2Book(models.Model):
    book_title = models.CharField(max_length=50)
    author = models.CharField(max_length=25)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.book_title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds the current date/time

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    

class Subscriber(models.Model):  # New model for newsletter subscribers
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class BookSearch(models.Model):
    name = models.CharField(max_length=255)  # Student's name
    email = models.EmailField()  # Student's email
    book_name = models.CharField(max_length=255)  # Name of the book
    search_date = models.DateTimeField(auto_now_add=True)  # Search timestamp

    def __str__(self):
        return f"{self.name} - {self.book_name}"