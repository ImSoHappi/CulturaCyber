from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import moduleModel, taskModel, activityModel
from culturacyberAuth.models import clientModel
from .forms import clientForm, moduleForm, activityForm, taskForm

@login_required(login_url='login')
def home(request):
    client = request.user.extend.client
    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()

    return render(request, 'culture_templates/home.html', context=context)

@login_required(login_url='login')
def client_admin(request):

    if 'edit_client' in request.POST:
        client = request.POST['client_pk']
        instance = get_object_or_404(clientModel, uuid=client)
        form = clientForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('client_admin')

    if 'add_client' in request.POST:
        form = clientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_admin')

    context = {}
    context['segment'] = 'admin'
    context['modules_list'] = moduleModel.get_all_modules()
    context['form'] = clientForm()
    context['client_list'] = clientModel.all_client_list()

    return render(request, 'culture_templates/client_admin.html', context=context)

@login_required(login_url='login')
def module_admin(request):

    if 'add_module' in request.POST:
        form = moduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_admin')

    context = {}
    context['segment'] = 'admin'
    context['modules_list'] = moduleModel.get_all_modules()
    context['form'] = moduleForm

    return render(request, 'culture_templates/module_admin.html', context=context)

@login_required(login_url='login')
def client_edit(request, client):

    edit_client = clientModel.get_client(client)

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['client'] = edit_client
    context['form'] = clientForm(initial={'name':edit_client.name ,'teamslink':edit_client.teamslink, 'description':edit_client.description, 'disabled':edit_client.disabled})

    return render(request, 'culture_templates/edit_client.html', context=context)

@login_required(login_url='login')
def module_client_list(request, module):
    
    if 'add_client_module' in request.POST:
        client = clientModel.get_client(request.POST['client_uuid'])
        module_add = moduleModel.get_module(module)
        module_add.client.add(client)
        module_add.save()

        return redirect('module_client_list', module=module)

    if 'remove_client_module' in request.POST:
        client = clientModel.get_client(request.POST['client_uuid'])
        module_add = moduleModel.get_module(module)
        module_add.client.remove(client)
        module_add.save()

        return redirect('module_client_list', module=module)

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

        if "add_task" in request.POST:
            form = taskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.activity = activityModel.get_activity(request.POST['activity'])
                task.save()
                return redirect('module_client', module=module, client=client)

        if "add_activity" in request.POST:
            form = activityForm(request.POST)
            client_act = clientModel.get_client(client)
            module_act = moduleModel.get_module(module)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.client = client_act
                activity.module = module_act
                if activityModel.first_activity(module, client):
                    activity.activity_status = 1
                activity.save()
                return redirect('module_client', module=module, client=client)

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
    context['form'] = taskForm

    return render(request, 'culture_templates/module_client.html', context=context)

   
@login_required(login_url='login')
def add_activity(request, module, client):

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['client'] = clientModel.get_client(client)
    context['form'] = activityForm

    return render(request, 'culture_templates/add_activity.html', context=context)
     