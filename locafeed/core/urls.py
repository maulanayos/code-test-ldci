from django.urls import path, include
from knox import views as knox_views
from . import views
from .api import (
    RegisterAPI, LoginAPI, UserAPI, UserProfileAPI,
    LocationListCreateAPI, LocationDetailAPI,
    PostListCreateAPI, PostDetailAPI
)

# Web URL patterns
web_urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('map/', views.map_view, name='map'),
    path('map/<int:post_id>/', views.map_view, name='map_with_post'),
    path('api-docs/', views.api_docs_view, name='api_docs'),
]

# API URL patterns
api_urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterAPI.as_view(), name='api_register'),
    path('auth/login/', LoginAPI.as_view(), name='api_login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='api_logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='api_logoutall'),
    path('auth/user/', UserAPI.as_view(), name='api_user'),
    path('auth/profile/', UserProfileAPI.as_view(), name='api_profile'),
    
    # Location endpoints
    path('locations/', LocationListCreateAPI.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationDetailAPI.as_view(), name='location-detail'),
    
    # Post endpoints
    path('posts/', PostListCreateAPI.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailAPI.as_view(), name='post-detail'),
]

# Combined URL patterns
urlpatterns = web_urlpatterns + [
    path('api/', include([(path('', include(api_urlpatterns)))]))  
]
