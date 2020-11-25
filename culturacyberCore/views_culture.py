from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import moduleModel, taskModel, activityModel
from culturacyberAuth.models import clientModel, userModel
from .forms import EditclientForm, AddclientForm, moduleForm, activityForm, taskForm
from culturacyberAuth.forms import userForm
from django.utils import timezone
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from culturacyberAuth.forms import mainuserForm
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):

    graph_today = timezone.now()
    graph_acitivity_by_month = []

    graph_months_list = []
    graph_activities = []

    for substract in range(10):
        target_time = graph_today - datetime.timedelta(substract*365/12)
        graph_activities.append(activityModel.get_activity_by_month(target_time.month, target_time.year))
        graph_months_list.append(target_time.strftime("%b %Y"))

    graph_months_list.reverse()
    graph_activities.reverse()

    client = request.user.extend.client
    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['rejected_tasks'] = taskModel.rejected_tasks()
    context['inprocess_tasks'] = taskModel.inprocess_tasks()
    context['finished_tasks'] = taskModel.finished_tasks()
    context['count_finished'] = taskModel.finished_tasks().count()
    context['count_inprocess'] = taskModel.inprocess_tasks().count()
    context['count_rejected'] = taskModel.rejected_tasks().count()
    context['total_task'] = taskModel.rejected_tasks().count() + taskModel.inprocess_tasks().count() + taskModel.finished_tasks().count()
    
    context['graph_month_list'] = graph_months_list
    context['graph_activities'] = graph_activities

    return render(request, 'culture_templates/home.html', context=context)

@login_required(login_url='login')
def client_admin(request):

    if request.method == "POST":

        if 'edit_client' in request.POST:
            client = request.POST['client_pk']
            instance = get_object_or_404(clientModel, uuid=client)
            form = EditclientForm(request.POST, instance=instance)

            if form.is_valid():
                form.save()
                return redirect('client_admin')

        if 'add_client' in request.POST:
            form = AddclientForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('client_admin')

        if 'desactivated_client' in request.POST:
            client = request.POST['client_pk']
            instance = get_object_or_404(clientModel, uuid=client)
            instance.disabled^=True
            instance.save()
            return redirect('client_admin')
            
    context = {}
    context['segment'] = 'admin'
    context['modules_list'] = moduleModel.get_all_modules()
    context['form'] = AddclientForm()
    context['client_list'] = clientModel.all_client_list()

    return render(request, 'culture_templates/client_admin.html', context=context)

@login_required(login_url='login')
def module_admin(request):

    if request.method == "POST":

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
    context['form'] = EditclientForm(initial={'name':edit_client.name ,'teamslink':edit_client.teamslink, 'description':edit_client.description, 'disabled':edit_client.disabled})

    return render(request, 'culture_templates/edit_client.html', context=context)

@login_required(login_url='login')
def module_client_list(request, module):
    
    if request.method == "POST":

        if 'edit_module' in request.POST:
            instance = get_object_or_404(moduleModel, uuid=module)
            form = moduleForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('module_client_list', module=module)

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
        ### Activities functions ###
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

        if 'edit_activity' in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            form = activityForm(request.POST, instance=activity)
            if form.is_valid():
                form.save()
                return redirect('module_client', module=module, client=client) 

        if "finish_activity" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            activity.activity_status = 0
            activity.save()
            next_activity = activityModel.get_next_activity(activity, client, module)
            if next_activity != "finish":
                next_activity.activity_status = 1
                next_activity.save()
            activity.activity_status = 0
            activity.save()

        if "waiting_activity" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            activity.activity_status = 2
            activity.save()

        if "inprocess_activity" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            activity.activity_status = 1
            activity.save()

        if "delete_activity" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            next_activity = activityModel.get_next_activity(activity, client, module)
            if next_activity != "finish":
                next_activity.activity_status = 1
                next_activity.save()
            activity.delete()

        ### Tasks functions ###
        if "edit_task" in request.POST:
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            form = taskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('module_client', module=module, client=client) 

        if "add_task" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            form = taskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.activity = activity
                task.updated_for = request.user.get_full_name()
                task.save()
                
                return redirect('module_client', module=module, client=client)  

        if "finish_task" in request.POST:
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            task.task_status = 0
            task.updated_for = request.user.get_full_name()
            task.save()
            if taskModel.all_task_finish(activity):
                next_activity = activityModel.get_next_activity(activity, client, module)
                if next_activity != "finish":
                    next_activity.activity_status = 1
                    next_activity.save()
                activity.activity_status = 0
                activity.save()

        if "corrected_task" in request.POST:
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            task.task_status = 2
            task.updated_for = request.user.get_full_name()
            task.save()
            activity.activity_status = 1
            activity.save()

        if "reject_task" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
            task.task_status = 3
            task.updated_for = request.user.get_full_name()
            task.save()
            activity.activity_status = 1
            activity.save()

        if "delete_task" in request.POST:
            activity = get_object_or_404(activityModel, pk=request.POST['activitypk'])
            task = get_object_or_404(taskModel, pk=request.POST['taskpk'])
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


@login_required(login_url='login')
def create_user(request):

    if request.method == "POST":

        if "create_user" in request.POST:
            mainform = mainuserForm(request.POST)
            form = userForm(request.POST)
            if mainform.is_valid():
                user = User.objects.create_user(mainform.cleaned_data['username'], mainform.cleaned_data['username'], mainform.cleaned_data['password1'])
                user.first_name = mainform.cleaned_data['first_name']
                user.last_name = mainform.cleaned_data['last_name']
                user.save()
                client = clientModel.get_client(form['client'].value())
                
                if 'is_cultureteam' in request.POST:
                    culture = True
                else:
                    culture = False

                if 'is_organizer' in request.POST:
                    orgnizer = True
                else:
                    orgnizer = False    

                userextend = userModel(user=user, client=client, is_cultureteam=culture , is_organizer=orgnizer)
                userextend.save()
                return redirect('create_user')
    
    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['form_user'] = userForm
    context['form'] = mainuserForm
    return render(request, 'culture_templates/create_user.html', context=context)


@login_required(login_url='login')
def edit_module(request, module):

    edit_module = moduleModel.get_module(module)
    
    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()

    context['form'] = moduleForm(initial={'name':edit_module.name ,'icon':edit_module.icon, 'description':edit_module.description})

    return render(request, 'culture_templates/edit_module.html', context=context)


@login_required(login_url='login')
def client_users_list(request, client):
    
    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()

    context['organizers_list'] = userModel.organizers_client_list(client)
    return render(request, 'culture_templates/client_users_list.html', context=context)


@login_required(login_url='login')
def edit_activity(request, module, client, activity):

    edit_activity = activityModel.get_activity(activity)

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['activity'] = activityModel.get_activity(activity)
    context['form'] = activityForm(initial={'name':edit_activity.name ,'programmed_date':edit_activity.programmed_date, 'description':edit_activity.description})

    return render(request, 'culture_templates/edit_activity.html', context=context)

@login_required(login_url='login')
def edit_task(request, task):

    edit_task = taskModel.get_task(task)

    context = {}
    context['segment'] = 'home'
    context['modules_list'] = moduleModel.get_all_modules()
    context['task'] = taskModel.get_task(task)
    context['form'] = taskForm(initial={'name':edit_task.name ,'task_status':edit_task.task_status, 'teamslink':edit_task.teamslink})

    return render(request, 'culture_templates/edit_task.html', context=context)

@login_required(login_url='login')
def add_survey(request):
    
    return render(request, 'add_survey.html')    
  