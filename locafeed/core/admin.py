from django.contrib import admin
from .models import Location, Post, UserProfile, UserSession

# Register models
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'location', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('text', 'author__username')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_private')
    list_filter = ('is_private',)
    search_fields = ('user__username', 'bio')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'device_type', 'browser', 'os', 'login_time', 'is_active')
    list_filter = ('is_active', 'device_type', 'browser', 'os', 'login_time')
    search_fields = ('user__username', 'ip_address')
    date_hierarchy = 'login_time'
    readonly_fields = ('user', 'session_key', 'ip_address', 'user_agent', 'device_type', 'browser', 'os', 'login_time', 'logout_time')
