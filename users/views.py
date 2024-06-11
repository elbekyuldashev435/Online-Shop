from django.shortcuts import render, redirect
from .models import CustomUser
from django.views import View
from .forms import UserForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class RegisterView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'auth/register.html', {'form': form})
    
    def post(self, request):
        form = UserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            return render(request, 'auth/register.html', {'form':form})
        

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'auth/login.html', {'form':login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home:home-page')
        else:
            return render(request, 'auth/login.html', {'form':login_form})
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home-page')

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile/profile.html')
    

class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'profile/profile_update.html', {'form':update_form})
    
    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            return redirect('users:profile')
        else:
            return render(request, 'profile/profile_update.html', {'form':update_form})
        
