from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Location, UserProfile


def home_view(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Login the user
                login(request, user)
                
                # Session is created automatically by the middleware
                
                messages.success(request, f'Welcome back, {username}!')
                
                # Get redirect URL or go to dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            # Detailed error message to help users understand the issue
            if 'username' in form.errors:
                messages.error(request, f'Username error: {form.errors["username"][0]}')
            elif 'password' in form.errors:
                messages.error(request, f'Password error: {form.errors["password"][0]}')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    """Registration page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    """Logout view"""
    # The session marking as inactive is handled by the middleware
    # when it detects a logout request
    
    # Standard Django logout
    logout(request)
    
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard page view"""
    posts_list = Post.objects.all().order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(Q(text__icontains=query) | Q(author__username__icontains=query))
    
    # Pagination - 5 posts per page as per requirement
    paginator = Paginator(posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def create_post_view(request):
    """Create new post view"""
    if request.method == 'POST':
        text = request.POST.get('text')
        location_name = request.POST.get('location_name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Validate post text (max 140 characters)
        if not text:
            messages.error(request, 'Post text is required.')
            return redirect('create_post')
            
        if len(text) > 140:
            messages.error(request, 'Post text must be 140 characters or less.')
            return redirect('create_post')
        
        # Validate location data
        if not all([location_name, latitude, longitude]):
            messages.error(request, 'Location information is required.')
            return redirect('create_post')
            
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            messages.error(request, 'Invalid location coordinates.')
            return redirect('create_post')
        
        # Create or get location
        location, created = Location.objects.get_or_create(
            name=location_name,
            defaults={'latitude': latitude, 'longitude': longitude}
        )
        
        # Create post
        post = Post.objects.create(
            author=request.user,
            text=text,
            location=location
        )
        
        messages.success(request, 'Post created successfully!')
        return redirect('dashboard')
    
    return render(request, 'core/create_post.html')


@login_required
def map_view(request, post_id=None):
    """Map view with post location"""
    if post_id:
        # Get specific post and center the map on it
        post = get_object_or_404(Post, id=post_id)
        posts = [post]
        center_post = post
    else:
        # Get all posts with locations
        posts = Post.objects.filter(location__isnull=False).order_by('-created_at')
        center_post = None
    
    context = {'posts': posts, 'center_post': center_post}
    return render(request, 'core/map.html', context)


@login_required
def profile_view(request):
    """User profile view"""
    if request.method == 'POST':
        # Handle profile update
        bio = request.POST.get('bio')
        date_of_birth = request.POST.get('date_of_birth')
        is_private = request.POST.get('is_private') == 'on'
        
        profile = request.user.profile
        profile.bio = bio
        if date_of_birth:
            profile.date_of_birth = date_of_birth
        profile.is_private = is_private
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'core/profile.html')


def api_docs_view(request):
    """API documentation view"""
    return render(request, 'core/api_docs.html')
