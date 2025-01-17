"""
URL configuration for bookmark_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookmarks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add/', views.add_bookmark, name='add_bookmark'),
    path('', views.list_bookmarks, name='list_bookmarks'),
    path('edit/<int:pk>/', views.edit_bookmark, name='edit_bookmark'),
    path('delete/<int:pk>/', views.delete_bookmark, name='delete_bookmark'),
    path('search/', views.search_bookmarks, name='search_bookmarks'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('signup/', views.signup, name='signup'),
]
