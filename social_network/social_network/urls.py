from django.contrib import admin
from django.urls import path, include
from posts import views

urlpatterns = [
    path('', views.post_list, name='home'),
    path('admin/', admin.site.urls),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_pk>/comments/', views.add_comment, name='add_comment'),
    path('posts/<int:post_pk>/like/', views.add_like, name='add_like'),
]