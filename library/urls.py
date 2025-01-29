from django.urls import path
from . import views
from .views import contact_view, contact_list_view
from django.shortcuts import redirect

urlpatterns = [
    path('',views.index,name = 'index'),
    path('', views.search_books, name='index'),  # For index.html
    path('students/', views.student_list, name='student_list'),
    path('s2books/', views.s2book_list, name='s2book_list'),
    path('news/', views.news_view, name='news'),
    path('about/', views.about, name = 'about'),
    path('contact/', contact_view, name='contact'),
    path('contact-list/', contact_list_view, name='contact_list'),  # New route for message listing
    path('register/', views.register, name='register'),  # Registration URL
    path('login/', views.login_view, name='login'),      # Login URL
    path('logout/', views.logout_view, name='logout'),    # Logout URL
    path('success/', views.letter_success, name='letter_success'),
    # Redirect from /accounts/login/ to /login/
    path('accounts/login/', lambda request: redirect('/login')),
    path('search_books/', views.search_books, name='search_books'),  # Register the view

]