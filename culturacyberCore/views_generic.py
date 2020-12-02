from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseServerError
from .models import moduleModel
from culturacyberAuth.models import userModel
from culturacyberAuth.forms import UpdateProfile
from django.contrib.auth.models import User

from culturacyberAuth.forms import loginForm

def login_view(request):

    if request.user.is_authenticated:
        return redirect('redirector')

    form = loginForm()
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('redirector')
            else:
                messages.error(request, "Credenciales incorrectas, intentalo de nuevo.", extra_tags="red" )

    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.error(request, "Has cerrado sesion correctamente.", extra_tags="green" )
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


def survey(request):
    return render(request, 'survey_templates/survey.html')


def my_profile(request):

    if request.method == "POST":
        
        if 'edit_user' in request.POST:
            form = UpdateProfile(request.POST, instance=request.user)
            if form.is_valid():
                print
                form.instance.username = form.cleaned_data['email']
                form.save()
                messages.success(request ,"La información se actualizo correctamente.", extra_tags="success")
                return redirect('my_profile')
            else:
                messages.error(request ,"La información no se ha podido actualizar.", extra_tags="error")
                return redirect('my_profile')
        
        if 'edit_user_pass' in request.POST:
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            if pass1 == pass2:
                user_update = User.objects.get(username=request.user.username)
                user_update.set_password(pass1)
                user_update.save()
                messages.success(request ,"La contraseña se actualizo correctamente, inicia sesion nuevamente con las nuevas credenciales.", extra_tags="green")
                return redirect('login')
            else:
                messages.error(request ,"La contraseña no se actualizo debido a que las contraseñas no son iguales", extra_tags="error")
                return redirect('my_profile')

    context = {}
    context['segment'] = 'my_profile'

    return render(request, 'generic_templates/my_profile.html')