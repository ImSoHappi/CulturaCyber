from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from culturacyberAuth.models import clientModel
from .models import moduleModel, taskModel, client_module_Model
from datetime import datetime

@login_required(login_url='login')
def home(request):

    client = request.user.extend.client
    context = {}
    context['segment'] = 'home'
    context['my_modules'] = clientModel.my_modules(client)
    context['recent_tasks'] = taskModel.get_calendar_task(client).order_by('-updated_at')[:6]
   
    return render(request, 'organizer_templates/home.html', context=context)

@login_required(login_url='login')
def module_detail(request, module):
    client = request.user.extend.client

    if request.method == "POST":
        if "finish_task" in request.POST:
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            task.task_status = 0
            task.save()
            return redirect('module_detail', module=module)

        if "reject_task" in request.POST:
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            task.task_status = 3
            task.save()
            return redirect('module_detail', module=module)

    context = {}
    context['my_activity'] = clientModel.my_activities(client, module)
    context['tasks'] = clientModel.my_tasks(client, module)
    context['segment'] = moduleModel.objects.get(uuid=module)
    context['my_modules'] = clientModel.my_modules(client)
    context['client'] = client
    context['rejected_task'] = taskModel.get_rejected_module_task(module, client).count()
    context['inprocess_task'] = taskModel.get_inprocess_module_task(module, client).count()
    context['finished_task'] = taskModel.get_finished_module_task(module, client).count()
    context['client_module'] = client_module_Model.get_client_module(module, client)

    return render(request, 'organizer_templates/module.html', context=context)