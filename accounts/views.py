from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User  # Добавляем этот импорт!
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .decorators import admin_required, manager_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} был создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профиль был обновлен!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'registration/profile.html', context)


@login_required
@admin_required
def user_management(request):
    # Получаем всех пользователей с их профилями
    users = User.objects.all().select_related('userprofile')
    
    # Статистика
    admin_count = users.filter(userprofile__role='admin').count()
    manager_count = users.filter(userprofile__role='manager').count()
    user_count = users.filter(userprofile__role='user').count()
    
    context = {
        'users': users,
        'admin_count': admin_count,
        'manager_count': manager_count,
        'user_count': user_count,
    }
    
    return render(request, 'accounts/user_management.html', context)

@login_required
@admin_required
def change_user_role(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        new_role = request.POST.get('role')
        
        if new_role in ['admin', 'manager', 'user']:
            user.userprofile.role = new_role
            user.userprofile.save()
            messages.success(request, f'Роль пользователя {user.username} изменена на {new_role}')
        else:
            messages.error(request, 'Неверная роль')
    
    return redirect('user_management')