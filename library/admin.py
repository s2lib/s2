from django.contrib import admin
from .models import Student, S2Book, Contact, Subscriber, BookSearch

# Register your models here.

admin.site.register(Student)
admin.site.register(S2Book)
admin.site.register(Subscriber)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'timestamp')
    search_fields = ('name', 'email')


@admin.register(BookSearch)
class BookSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'book_name', 'search_date')