from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as auth_views
from posts import views as posts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', posts_views.post_list, name='post_list'),
    path('posts/<int:pk>/', posts_views.post_detail, name='post_detail'),
    path('posts/<int:post_pk>/comments/', posts_views.add_comment, name='add_comment'),
    path('posts/<int:post_pk>/like/', posts_views.add_like, name='add_like'),
    path('register/', posts_views.register_user, name='register'),  
    path('api-token-auth/', auth_views.obtain_auth_token, name='api_token_auth'), 
    path('api-auth/', include('rest_framework.urls')),  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
