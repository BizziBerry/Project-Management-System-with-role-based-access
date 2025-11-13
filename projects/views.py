from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm
from accounts.decorators import admin_required, manager_required

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'tasks': tasks
    })

@login_required
@manager_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Проект успешно создан!')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Создать проект'})

@login_required
@manager_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект успешно обновлен!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Редактировать проект'})

@login_required
@admin_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект успешно удален!')
        return redirect('project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def task_list(request):
    tasks = Task.objects.all()
    
    # Статистика для отображения в шаблоне
    tasks_done_count = tasks.filter(status='done').count()
    tasks_in_progress_count = tasks.filter(status='in_progress').count()
    tasks_todo_count = tasks.filter(status='todo').count()
    
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'tasks_done_count': tasks_done_count,
        'tasks_in_progress_count': tasks_in_progress_count,
        'tasks_todo_count': tasks_todo_count,
    })

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comments.all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('task_detail', pk=task.pk)
    else:
        comment_form = CommentForm()
    
    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
@manager_required
def task_create(request, project_pk=None):
    project = None
    if project_pk:
        project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            if project:
                task.project = project
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('task_detail', pk=task.pk)
    else:
        initial = {'project': project} if project else {}
        form = TaskForm(initial=initial)
    
    context = {
        'form': form, 
        'title': 'Создать задачу',
        'project': project
    }
    return render(request, 'tasks/task_form.html', context)

@login_required
@manager_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Редактировать задачу'})

@login_required
@manager_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('project_detail', pk=task.project.pk)
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.user.userprofile.is_user() and task.assigned_to != request.user:
        return HttpResponseForbidden("Вы не можете завершить эту задачу")
    
    task.status = 'done'
    task.save()
    messages.success(request, 'Задача отмечена как выполненная!')
    return redirect('task_detail', pk=task.pk)