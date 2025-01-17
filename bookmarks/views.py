from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Bookmark
from .forms import SignUpForm, BookmarkForm
from django.core.paginator import Paginator
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_bookmarks')
    else:
        form = SignUpForm()
    return render(request, 'bookmarks/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list_bookmarks')
    else:
        form = AuthenticationForm()
    return render(request, 'bookmarks/login.html', {'form': form})
@login_required(login_url='login/')
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='login/')
def add_bookmark(request):
    if request.method == 'POST':                                                                            
        form = BookmarkForm(request.POST)
        if form.is_valid():
            if Bookmark.objects.filter(user=request.user).count() < 5:
                bookmark = form.save(commit=False)
                bookmark.user = request.user
                bookmark.save()
                return redirect('list_bookmarks')
            else:
                return render(request, 'bookmarks/add_bookmark.html', {'form': form, 'error': 'You can only add 5 bookmarks.'})
    else:
        form = BookmarkForm()
    return render(request, 'bookmarks/add_bookmark.html', {'form': form})

@login_required(login_url='login/')
def list_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    paginator = Paginator(bookmarks, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookmarks/list_bookmarks.html', {'page_obj': page_obj})

@login_required(login_url='login/')
def edit_bookmark(request, pk):
    bookmark = Bookmark.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return redirect('list_bookmarks')
    else:
        form = BookmarkForm(instance=bookmark)
    return render(request, 'bookmarks/edit_bookmark.html', {'form': form})

@login_required(login_url='login/')
def delete_bookmark(request, pk):
    bookmark = Bookmark.objects.get(pk=pk, user=request.user)
    bookmark.delete()
    return redirect('list_bookmarks')

@login_required(login_url='login/')
def search_bookmarks(request):
    query = request.GET.get('q')
    if query:
        bookmarks = Bookmark.objects.filter(user=request.user, title__icontains=query)
    else:
        bookmarks = Bookmark.objects.filter(user=request.user)
    return JsonResponse({'bookmarks': list(bookmarks.values())})