from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import moduleModel, taskModel, activityModel
from culturacyberAuth.models import clientModel
from .forms import clientForm

@login_required(login_url='login')
def home(request):

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()

    return render(request, 'culture_templates/home.html', context=context)

@login_required(login_url='login')
def client_admin(request):

    if 'edit_client' in request.POST:
        edit_client = clientForm(request.POST)

        if edit_client.is_valid():
            client = request.POST['client_pk']
            client_edit = clientModel.objects.get(uuid=client)
            client_edit.name = edit_client.cleaned_data['name']
            client_edit.description = edit_client.cleaned_data['description']
            client_edit.save()

            return redirect('client_admin')

    if 'add_client' in request.POST:
        form = clientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_admin')

    context = {}
    context['segment'] = 'admin'
    context['modules_list'] = moduleModel.get_all_modules()
    context['form'] = clientForm
    context['client_list'] = clientModel.client_list()

    return render(request, 'culture_templates/client_admin.html', context=context)

@login_required(login_url='login')
def client_edit(request, client):

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['client'] = clientModel.get_client(client)

    return render(request, 'culture_templates/edit_client.html', context=context)

@login_required(login_url='login')
def module_client_list(request, module):
    
    context = {}
    context['segment'] = moduleModel.objects.get(uuid=module)
    context['modules_list'] = moduleModel.get_all_modules()
    context['module_detail'] = moduleModel.get_module(module)
    context['active_client'] = clientModel.active_model_clients(module)
    context['disable_client'] = clientModel.disable_model_clients(module)

    return render(request, 'culture_templates/module_client_list.html', context=context)

@login_required(login_url='login')
def module_client(request, module, client):

    if request.method == "POST":
        task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
        activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])

        if "finish_task" in request.POST:
            task.task_status = 0
            task.save()
            if taskModel.all_task_finish(activity):
                next_activity = activityModel.get_next_activity(activity, client, module)
                if next_activity != "finish":
                    next_activity.activity_status = 1
                    next_activity.save()
                activity.activity_status = 0
                activity.save()

        if "corrected_task" in request.POST:
            task.task_status = 2
            task.save()
            activity.activity_status = 1
            activity.save()

        if "reject_task" in request.POST:
            task.task_status = 3
            task.save()
            activity.activity_status = 1
            activity.save()

        if "delete_task" in request.POST:
            task.delete()

            if taskModel.all_task_finish(activity):
                next_activity = activityModel.get_next_activity(activity, client, module)
                next_activity.activity_status = 1
                next_activity.save()
                activity.activity_status = 0
                activity.save()
        
        return redirect('module_client', module=module, client=client)

    context = {}
    context['segment'] = moduleModel.objects.get(uuid=module)
    context['modules_list'] = moduleModel.get_all_modules()
    context['client'] = clientModel.get_client(client)
    context['client_activities'] = clientModel.my_activities(client, module)
    context['client_tasks'] = clientModel.my_tasks(client, module)

    return render(request, 'culture_templates/module_client.html', context=context)