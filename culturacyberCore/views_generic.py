from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseServerError

from culturacyberAuth.forms import FormLogin

def login_view(request):

    if request.user.is_authenticated:
        return redirect('redirector')

    form = FormLogin()
    if request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('redirector')
            else:
                # Return an 'invalid login' error message.
                ...

    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def redirector(request):
    # Check user permissions
    user = request.user.extend
    if user.is_cultureteam:
        # Send to culture home
        return redirect('culture_home')
    if user.is_organizer:
        # Send to organizer home
        return redirect('organizer_home')
        
    return HttpResponseServerError()