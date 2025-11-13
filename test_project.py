#!/usr/bin/env python
"""
Упрощенный скрипт для тестирования основных функций ProjectFlow
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

def test_basic_functionality():
    """Тест базовой функциональности"""
    from django.contrib.auth.models import User
    from projects.models import Project, Task
    from accounts.models import UserProfile
    
    print("🧪 ТЕСТИРОВАНИЕ БАЗОВОЙ ФУНКЦИОНАЛЬНОСТИ")
    print("=" * 50)
    
    # 1. Тест создания пользователя и профиля
    print("1. Тест создания пользователя...")
    user = User.objects.create_user('test_user', 'test@test.com', 'test123')
    assert hasattr(user, 'userprofile')
    assert user.userprofile.role == 'user'
    print("   ✅ Пользователь и профиль созданы")
    
    # 2. Тест создания проекта
    print("2. Тест создания проекта...")
    project = Project.objects.create(
        title='Test Project',
        description='Test Description',
        created_by=user
    )
    assert project.title == 'Test Project'
    assert project.created_by == user
    print("   ✅ Проект создан")
    
    # 3. Тест создания задачи
    print("3. Тест создания задачи...")
    assigned_user = User.objects.create_user('assigned_user', 'assigned@test.com', 'test123')
    task = Task.objects.create(
        title='Test Task',
        project=project,
        assigned_to=assigned_user,
        created_by=user
    )
    assert task.title == 'Test Task'
    assert task.assigned_to == assigned_user
    print("   ✅ Задача создана")
    
    # 4. Тест бизнес-логики
    print("4. Тест бизнес-логики...")
    assert task.can_user_complete(assigned_user) == True
    assert task.can_user_complete(user) == False
    print("   ✅ Бизнес-логика работает")
    
    # 5. Тест ролевой модели
    print("5. Тест ролевой модели...")
    admin_user = User.objects.create_user('admin_user', 'admin@test.com', 'test123')
    admin_profile = admin_user.userprofile
    admin_profile.role = 'admin'
    admin_profile.save()
    
    manager_user = User.objects.create_user('manager_user', 'manager@test.com', 'test123')
    manager_profile = manager_user.userprofile
    manager_profile.role = 'manager'
    manager_profile.save()
    
    assert admin_profile.is_admin() == True
    assert manager_profile.is_manager() == True
    assert user.userprofile.is_user() == True
    print("   ✅ Ролевая модель работает")
    
    print("=" * 50)
    print("🎉 ВСЕ ОСНОВНЫЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 50)

def test_web_access():
    """Тест доступа к веб-страницам"""
    from django.test import Client
    from django.urls import reverse
    
    print("\n🌐 ТЕСТИРОВАНИЕ ВЕБ-ДОСТУПА")
    print("=" * 50)
    
    client = Client()
    
    # 1. Тест неавторизованного доступа
    print("1. Тест неавторизованного доступа...")
    response = client.get(reverse('project_list'))
    assert response.status_code == 302  # Редирект на логин
    print("   ✅ Неавторизованный доступ ограничен")
    
    # 2. Тест авторизованного доступа
    print("2. Тест авторизованного доступа...")
    User = django.contrib.auth.models.User
    user = User.objects.create_user('web_user', 'web@test.com', 'test123')
    client.login(username='web_user', password='test123')
    
    response = client.get(reverse('project_list'))
    assert response.status_code == 200
    print("   ✅ Авторизованный доступ разрешен")
    
    print("=" * 50)
    print("🎉 ВЕБ-ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 50)

if __name__ == '__main__':
    try:
        test_basic_functionality()
        test_web_access()
        print("\n✅ ПРОЕКТ PROJECTFLOW РАБОТАЕТ КОРРЕКТНО!")
        exit(0)
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        exit(1)