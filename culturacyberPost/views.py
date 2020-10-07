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

    context = {}
    context['segment'] = 'admin'
    context['form'] = postForm
    return render(request, 'post/add_post.html', context=context)

@login_required(login_url='login')
def post_detail(request, post_uuid):

    if request.method == 'POST':
        form = attachedForm(request.POST, request.FILES)
        
        if form.is_valid():

            attached = form.save(commit=False)
            attached.post = postModel.objects.get(uuid=post_uuid)
            attached.save()
            
            return redirect( 'post_detail', post_uuid )

    else:
        form = attachedForm()

    context = {}
    context['segment'] = 'home'
    context['files'] = attachedModel.objects.filter(post=post_uuid)
    context['post'] = postModel.objects.get(uuid=post_uuid)
    return render(request, 'post/post_detail.html', context=context)

@login_required(login_url='login')
def add_attached(request, post_uuid):

    context = {}
    context['segment'] = 'admin'
    context['post'] = postModel.objects.get(uuid=post_uuid)
    context['form'] = attachedForm
    return render(request, 'post/add_attached.html', context=context)