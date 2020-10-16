from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)

        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['email'])

        if len(user) > 0:
            messages.error(request,'Email is already in use!',extra_tags='email')
            return redirect('/')

        pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')
    
    else:
        return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request,'Invalid Email/Password',extra_tags='login_email')
            return redirect('/')

        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request,'Invalid Email/Password',extra_tags='login_password')
            return redirect('/')

        request.session['user_id'] = user[0].id
        return redirect('/dashboard')

    else:
        return redirect('/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_the_books': Book.objects.all(),
            'all_the_users': User.objects.all()
        }
        return render(request, 'dashboard.html', context)

def go_back(request):
    return redirect('/dashboard')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')


def add_a_book(request):
    if request.method == 'POST':
        errors = Book.objects.add_book_validator(request.POST)
        print(errors)
        if len(errors) > 0:
            print(errors)
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect('/dashboard')
        Book.objects.create(
            title=request.POST['book_title'],
            author=request.POST['book_author'],
            desc=request.POST['book_desc'],
            uploaded_by=User.objects.get(id=request.session['user_id']),
        )
        this_book = Book.objects.last()
        this_book.users_who_like.add(User.objects.get(id=request.session['user_id']))
        return redirect('/dashboard')
    else:
        return redirect('/logout')


def dashboard_faves(request, book_id, user_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=user_id)
    user.liked_books.add(book)
    print(user.liked_books)
    return redirect('/dashboard')


def show_book(request, book_id):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'book': Book.objects.get(id=book_id)
    }
    return render(request, 'show_book.html', context)


def update_book(request, book_id):
    context = {
        'book': Book.objects.get(id=book_id)
    }
    book = Book.objects.get(id=book_id)
    book.title = request.POST['update_book_title']
    book.desc = request.POST['update_book_desc']
    book.save()
    return redirect(f'/books/{ book.id }')


def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/dashboard')


def add_to_favorites(request, book_id, user_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=user_id)
    user.liked_books.add(book)
    print(user.liked_books)
    return redirect(f'/books/{ book.id }')


def unfavorite(request, book_id, user_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=user_id)
    user.liked_books.remove(book)
    print(user.liked_books)
    return redirect(f'/books/{ book.id }')