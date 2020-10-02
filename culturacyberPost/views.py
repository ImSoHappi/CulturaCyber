from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import *

# Create your views here.

@login_required(login_url='login')
def add_post(request):

    if request.method == 'POST':
        form = postForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return redirect('home')

    else:
        form = postForm()
        print("falle")

    context = {}
    context['segment'] = 'admin'
    context['form'] = postForm
    return render(request, 'post/add_post.html', context=context)