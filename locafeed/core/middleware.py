import re
from django.utils import timezone
from .models import UserSession

class UserSessionMiddleware:
    """
    Middleware to track user sessions and store login information
    such as IP address, user agent, and login/logout times
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Process request before view is called
        if request.user.is_authenticated:
            # Get or create a session for the user
            session_key = request.session.session_key
            
            # Try to get existing session for this session key
            user_session = UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).first()
            
            if not user_session:
                # Create new session entry
                user_session = UserSession(
                    user=request.user,
                    session_key=session_key,
                    ip_address=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                )
                
                # Parse user agent to determine device, browser, os
                user_session.device_type = self._get_device_type(request)
                user_session.browser = self._get_browser(request)
                user_session.os = self._get_os(request)
                
                # Get location information if available
                # This would typically involve a GeoIP lookup service
                # For now, we'll leave these fields empty
                
                user_session.save()
        
        # Process the request
        response = self.get_response(request)
        
        # Process response
        if request.user.is_authenticated and '/logout/' in request.path_info:
            # Mark all active sessions for this user as inactive
            UserSession.objects.filter(
                user=request.user,
                is_active=True
            ).update(
                is_active=False,
                logout_time=timezone.now()
            )
        
        return response
    
    def _get_client_ip(self, request):
        """Get the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_device_type(self, request):
        """Determine the device type based on user agent"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            return 'mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'tablet'
        else:
            return 'desktop'
    
    def _get_browser(self, request):
        """Determine the browser based on user agent"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if 'chrome' in user_agent and 'chromium' not in user_agent:
            return 'Chrome'
        elif 'firefox' in user_agent:
            return 'Firefox'
        elif 'safari' in user_agent and 'chrome' not in user_agent:
            return 'Safari'
        elif 'edge' in user_agent:
            return 'Edge'
        elif 'opera' in user_agent or 'opr' in user_agent:
            return 'Opera'
        elif 'msie' in user_agent or 'trident' in user_agent:
            return 'Internet Explorer'
        else:
            return 'Unknown'
    
    def _get_os(self, request):
        """Determine the operating system based on user agent"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if 'windows' in user_agent:
            return 'Windows'
        elif 'macintosh' in user_agent or 'mac os' in user_agent:
            return 'MacOS'
        elif 'linux' in user_agent and 'android' not in user_agent:
            return 'Linux'
        elif 'android' in user_agent:
            return 'Android'
        elif 'ios' in user_agent or 'iphone' in user_agent or 'ipad' in user_agent:
            return 'iOS'
        else:
            return 'Unknown'
