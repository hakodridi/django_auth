from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


def check_user_logged_in(request):
    if request.user.is_authenticated:
        return redirect('index')

@login_required
def index(request):
    return render(request, 'index.html', {})

def user_login(request):
    check_user_logged_in(request)
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



def user_signup(request):
    check_user_logged_in(request)
    if request.method == 'POST':
        full_name = request.POST.get('full-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.last_name = ''
        user.save()

        # Log in the user
        login(request, user)
        return redirect('index')

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'reset-password.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            print('An email has been sent with instructions to reset your password.')
            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'forgot-password.html', {'form': form})

def terms(request):
    return render(request, 'terms.html', {})


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].input_label = "Old Password"
        self.fields['new_password1'].input_label = "New Password"
        self.fields['new_password2'].input_label = "Confirm New Password"