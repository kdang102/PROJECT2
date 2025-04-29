from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import PasswordResetForm

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',{'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html',{'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',{'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',{'template_data': template_data})

def password_reset(request):
    template_data = {}
    template_data['title'] = 'Password Reset'
    if request.method == 'GET':
        form = PasswordResetForm()
        return render(request, 'accounts/password_reset.html', {'template_data': template_data, 'form': form})
    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                template_data['error'] = 'The username does not exist.'
                return render(request, 'accounts/password_reset.html', {'template_data': template_data, 'form': form})

            new_password = form.cleaned_data['new_password']
            user.password = make_password(new_password)
            user.save()

            template_data['success'] = 'Your password has been successfully reset.'
            return redirect('home.index')

        template_data['error'] = 'Please correct the errors below.'
        return render(request, 'accounts/password_reset.html', {'template_data': template_data, 'form': form})