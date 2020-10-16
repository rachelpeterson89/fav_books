from django.db import models
from datetime import date,datetime
import re


class UserManager(models.Manager):

    def reg_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First Name must be at least 3 characters!'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last Name must be at least 3 characters!'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters!'
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = 'Passwords do not match!'
        return errors
    
    def login_validator(self,postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = 'Invalid Email/Password'
        if len(postData['login_password']) <8:
            errors['login_password'] = 'Invalid Email/Password'
        return errors


class BookManager(models.Manager):

    def add_book_validator(self,postData):
        errors={}
        if len(postData['book_title']) < 3:
            errors['book_title'] = 'Book must have a title!'
        if len(postData['book_author']) < 3:
            errors['book_author'] = 'Book must have an author!'
        if len(postData['book_desc']) < 10:
            errors['book_desc'] = 'Description must be at least 10 characters!'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded",  on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()