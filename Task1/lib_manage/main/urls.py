from django.urls import path
from django.contrib import admin
from main import views

urlpatterns =[
  path("user", views.nominee, name='nominee'),
  path("", views.login_user, name='login'),
  path("logout", views.logout_user, name='logout'),
  path("register", views.register_user, name='register'),
  path("<int:n>", views.book_main, name='book'),
  path("books_user", views.borrowed, name='borrowed'),
  path("<int:n>/review", views.review, name='review'),
  path("booklist", views.booklist, name='booklist'),
  path("lib", views.librarian, name='librarian'),
  path("pending_requests", views.pending, name='pending'),
  path("dues", views.dues, name='dues'),
  path("addbook", views.addbook, name='addbook'),
  path("alterbook",views.alterbook,name="alterbook"),
  path("<int:n>/modifyform",views.modifyform,name="modifyform"),
]