#!/usr/bin/env python
"""
Демонстрационный скрипт для показа возможностей ProjectFlow
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import Project, Task
from accounts.models import UserProfile

def showcase_role_differences():
    """Демонстрация различий между ролями"""
    print("🎭 ДЕМОНСТРАЦИЯ РОЛЕВЫХ РАЗЛИЧИЙ")
    print("=" * 50)
    
    # Получаем демо-пользователей
    try:
        admin = User.objects.get(username='admin_demo')
        manager = User.objects.get(username='manager_demo')
        user = User.objects.get(username='alex_dev')
        
        print("👥 Демо-пользователи:")
        print(f"   👑 Администратор: {admin.username} ({admin.userprofile.role})")
        print(f"   👔 Менеджер: {manager.username} ({manager.userprofile.role})")
        print(f"   👤 Пользователь: {user.username} ({user.userprofile.role})")
        
        print("\n🔐 Права доступа:")
        print(f"   Администратор может:")
        print("   ✅ Управлять всеми пользователями")
        print("   ✅ Создавать/редактировать/удалять проекты")
        print("   ✅ Создавать/редактировать/удалять задачи")
        print("   ✅ Просматривать все данные")
        
        print(f"\n   Менеджер может:")
        print("   ✅ Создавать/редактировать проекты")
        print("   ✅ Создавать/редактировать/удалять задачи") 
        print("   ✅ Назначать задачи пользователям")
        print("   ❌ Удалять проекты")
        print("   ❌ Управлять пользователями")
        
        print(f"\n   Пользователь может:")
        print("   ✅ Просматривать проекты и задачи")
        print("   ✅ Завершать назначенные ему задачи")
        print("   ✅ Оставлять комментарии к задачам")
        print("   ❌ Создавать проекты и задачи")
        print("   ❌ Редактировать чужие задачи")
        
    except User.DoesNotExist:
        print("❌ Демо-пользователи не найдены. Запустите сначала demo_setup.py")

def showcase_projects_and_tasks():
    """Демонстрация проектов и задач"""
    print("\n📊 ДЕМОНСТРАЦИЯ ПРОЕКТОВ И ЗАДАЧ")
    print("=" * 50)
    
    projects = Project.objects.all()
    print(f"📂 Всего проектов: {projects.count()}")
    
    for project in projects:
        tasks = project.tasks.all()
        print(f"\n🏢 Проект: {project.title}")
        print(f"   📝 Описание: {project.description[:80]}...")
        print(f"   📊 Статус: {project.get_status_display()}")
        print(f"   ✅ Задач: {tasks.count()}")
        
        for task in tasks[:3]:  # Показываем первые 3 задачи
            status_icon = "🟢" if task.status == 'done' else "🟡" if task.status == 'in_progress' else "⚪"
            priority_icon = "🔴" if task.priority == 'high' else "🟡" if task.priority == 'medium' else "🔵"
            
            print(f"   {status_icon} {priority_icon} {task.title}")
            print(f"      👤 Назначена: {task.assigned_to.username if task.assigned_to else 'Не назначена'}")
            print(f"      📅 Срок: {task.due_date if task.due_date else 'Не установлен'}")
            print(f"      💬 Комментариев: {task.comments.count()}")

def showcase_business_logic():
    """Демонстрация бизнес-логики"""
    print("\n⚙️ ДЕМОНСТРАЦИЯ БИЗНЕС-ЛОГИКИ")
    print("=" * 50)
    
    try:
        user = User.objects.get(username='alex_dev')
        tasks = Task.objects.filter(assigned_to=user)
        
        print(f"👤 Задачи пользователя {user.username}:")
        for task in tasks:
            can_complete = task.can_user_complete(user)
            status = "✅ МОЖЕТ завершить" if can_complete else "❌ НЕ МОЖЕТ завершить"
            
            print(f"   📋 {task.title}")
            print(f"      {status}")
            print(f"      Статус: {task.get_status_display()}")
            print(f"      Проект: {task.project.title}")
            
            if not can_complete and task.status != 'done':
                print(f"      💡 Причина: задача не назначена на этого пользователя")

    except User.DoesNotExist:
        print("❌ Демо-пользователь не найден")

def showcase_api_capabilities():
    """Демонстрация возможностей API"""
    print("\n🔗 ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ API")
    print("=" * 50)
    
    print("🌐 Доступные API эндпоинты:")
    print("   📍 GET/POST    /api/projects/     - Проекты")
    print("   📍 GET/POST    /api/tasks/        - Задачи") 
    print("   📍 GET/POST    /api/comments/     - Комментарии")
    print("   📍 GET         /api/users/        - Пользователи (только админ)")
    print("   📍 POST        /api/auth/register/ - Регистрация")
    print("   📍 POST        /api/auth/login/    - Вход")
    print("   📍 POST        /api/auth/token/    - Получение токена")
    
    print("\n🔐 Аутентификация в API:")
    print("   Используйте Token authentication:")
    print('   Header: Authorization: Token "your_token_here"')
    
    print("\n💡 Пример запроса:")
    print('   curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/projects/')

def main():
    """Основная функция демонстрации"""
    print("🎪 ДЕМОНСТРАЦИЯ ВОЗМОЖНОСТЕЙ PROJECTFLOW")
    print("=" * 60)
    
    showcase_role_differences()
    showcase_projects_and_tasks() 
    showcase_business_logic()
    showcase_api_capabilities()
    
    print("\n" + "=" * 60)
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    print("\n🚀 ДЛЯ ТЕСТИРОВАНИЯ:")
    print("   1. Запустите сервер: python manage.py runserver")
    print("   2. Откройте http://127.0.0.1:8000/")
    print("   3. Войдите под разными пользователями")
    print("   4. Протестируйте функциональность!")

if __name__ == '__main__':
    main()