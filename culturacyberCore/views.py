from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from culturacyberPost.models import *

# Create your views here.

@login_required(login_url='login')
def home(request):

    context = {}
    context['segment'] = 'home'
    context['post_list'] = postModel.objects.all()
    return render(request, 'home.html', context=context)


@login_required(login_url='login')
def survey_list(request):

    context = {}
    context['segment'] = 'surveys'
    return render(request, 'survey_list.html', context=context)


@login_required(login_url='login')
def add_survey(request):

    context = {}
    context['segment'] = 'admin'
    return render(request, 'add_survey.html', context=context)


@login_required(login_url='login')
def survey_detail(request):

    context = {}
    context['segment'] = 'surveys'
    return render(request, 'survey_detail.html', context=context)