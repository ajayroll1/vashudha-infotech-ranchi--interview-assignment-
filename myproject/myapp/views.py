from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserLoginForm

def home(request):
    """Homepage view - redirect to login if not authenticated"""
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'homepage.html')

def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Try to authenticate with email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
    else:
        form = UserLoginForm()
    
    return render(request, 'login_Registerpage.html', {'form': form, 'form_type': 'login'})

def register_view(request):
    """Registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Check if email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
            else:
                user = form.save()
                login(request, user)
                messages.success(request, f'Welcome to Premium Estate, {user.first_name}!')
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'login_Registerpage.html', {'form': form, 'form_type': 'register'})

def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def dashboard(request):
    """Dashboard view - only for authenticated users"""
    return render(request, 'dashboard.html', {'user': request.user})
