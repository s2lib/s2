from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, BookSearchForm
from django.conf import settings
from .models import Student, S2Book, Contact, Subscriber, BookSearch
from django.contrib import messages
from .news_api import get_news
import requests
from django.urls import reverse


# Create your views here.

def index(request):
    """
    Handles the home page with a subscription form and an optional contact form.
    """
    if request.method == 'POST':
        if 'name' in request.POST:  # Handle contact form submission
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent successfully!")
            return redirect('letter_success')

        elif 'book_name' in request.POST:  # Handle book search form submission
            book_name = request.POST.get('book_name')
            email = request.POST.get('email')
            
            if book_name and email:
                # Optionally save the search query to the database
                BookSearch.objects.create(book_name=book_name, email=email)

                # Redirect to the search_books page with the query parameters
                return redirect(f"{reverse('search_books')}?book_name={book_name}&email={email}")
            else:
                messages.error(request, "Both book name and email are required.")

        elif 'email' in request.POST:  # Handle newsletter subscription
            email = request.POST.get('email')
            if email:
                if not Subscriber.objects.filter(email=email).exists():
                    Subscriber.objects.create(email=email)
                    messages.success(request, "Successfully subscribed to our newsletter!")
                    return redirect('letter_success') # Redirect to subscription success page
                else:
                    messages.warning(request, "You're already subscribed.")

    return render(request, 'index.html')

def letter_success(request):
    """
    Displays a success page after subscription.
    """
    return render(request, 'success.html')

def student_list(request):
    """
    Displays a list of all students.
    """
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def about(request):
    """
    Displays the about page.
    """
    return render(request, 'about.html')

def contact_view(request):
    """
    Handles the standalone contact form page.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the message to the database
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()

        # Use Django messages framework to send feedback to the user
        messages.success(request, "Your message has been sent successfully!")

        # Redirect back to the homepage
        return redirect('index')

    return render(request, 'contact_me.html')

@login_required
def contact_list_view(request):
    """
    Displays all contact messages for admins.
    """
    messages = Contact.objects.all().order_by('-timestamp')
    return render(request, 'contact_list.html', {'messages': messages})

#login logout register below!

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally, send a welcome email here
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('index')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Not Registered with us.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')


def s2book_list(request):
    s2books = S2Book.objects.all()
    return render(request, 's2book_list.html', {'s2books': s2books})

def news_view(request):
    news_articles = get_news() # Fetch news articles from the API
    return render(request, 'news.html', {"news_articles": news_articles})


def search_books(request):
    result = None
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            form.save()  # Save to the database

            # Fetch book search term
            book_name = form.cleaned_data['book_name']

            # Perform search via Open Library API
            api_url = f"https://openlibrary.org/search.json?q={book_name}"
            response = requests.get(api_url)
            if response.status_code == 200:
                result = response.json().get('docs', [])
    elif request.method == 'GET' and 'book_name' in request.GET:
        # Handle redirection from the `index` page
        book_name = request.GET.get('book_name')
        email = request.GET.get('email')

        # Save the data to the database
        BookSearch.objects.create(name='Anonymous', email=email, book_name=book_name)

        # Perform search via Open Library API
        api_url = f"https://openlibrary.org/search.json?q={book_name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            result = response.json().get('docs', [])
        form = BookSearchForm(initial={'book_name': book_name, 'email': email})
    else:
        form = BookSearchForm()

    return render(request, 'search_books.html', {'form': form, 'result': result})
