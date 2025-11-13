#!/usr/bin/env python
"""
Скрипт для настройки демонстрационных данных ProjectFlow
"""

import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import Project, Task, Comment
from accounts.models import UserProfile

def create_demo_users():
    """Создание демонстрационных пользователей"""
    print("👥 Создание демонстрационных пользователей...")
    
    users_data = [
        {'username': 'admin_demo', 'password': 'admin123', 'role': 'admin', 'email': 'admin@demo.com'},
        {'username': 'manager_demo', 'password': 'manager123', 'role': 'manager', 'email': 'manager@demo.com'},
        {'username': 'alex_dev', 'password': 'user123', 'role': 'user', 'email': 'alex@demo.com'},
        {'username': 'maria_design', 'password': 'user123', 'role': 'user', 'email': 'maria@demo.com'},
        {'username': 'john_qa', 'password': 'user123', 'role': 'user', 'email': 'john@demo.com'},
    ]
    
    created_users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            
            profile = user.userprofile
            profile.role = user_data['role']
            profile.save()
            
            created_users[user_data['role']] = user
            print(f"   ✅ Создан: {user.username} ({user_data['role']})")
        else:
            created_users[user_data['role']] = user
            print(f"   ⚠️ Уже существует: {user.username}")
    
    return created_users

def create_demo_projects(manager):
    """Создание демонстрационных проектов"""
    print("\n📊 Создание демонстрационных проектов...")
    
    projects_data = [
        {
            'title': 'Разработка корпоративного портала',
            'description': 'Создание современного веб-портала для сотрудников компании с системой документооборота и коммуникации.',
            'status': 'active'
        },
        {
            'title': 'Мобильное приложение для заказов',
            'description': 'Разработка кроссплатформенного мобильного приложения для iOS и Android с системой онлайн-заказов и оплаты.',
            'status': 'active'
        },
        {
            'title': 'Обновление CRM системы',
            'description': 'Модернизация существующей CRM системы с добавлением аналитики и интеграцией с мессенджерами.',
            'status': 'in_progress'
        },
        {
            'title': 'Внедрение системы аналитики',
            'description': 'Настройка системы сбора и анализа бизнес-метрик для отделов маркетинга и продаж.',
            'status': 'on_hold'
        }
    ]
    
    created_projects = []
    for project_data in projects_data:
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults={
                'description': project_data['description'],
                'status': project_data['status'],
                'created_by': manager
            }
        )
        if created:
            created_projects.append(project)
            print(f"   ✅ Создан проект: {project.title}")
        else:
            created_projects.append(project)
            print(f"   ⚠️ Проект уже существует: {project.title}")
    
    return created_projects

def create_demo_tasks(projects, users):
    """Создание демонстрационных задач"""
    print("\n✅ Создание демонстрационных задач...")
    
    tasks_data = [
        # Проект 1: Корпоративный портал
        {
            'title': 'Дизайн пользовательского интерфейса',
            'description': 'Разработать современный и интуитивно понятный UI для главной страницы и личного кабинета.',
            'project': 0, 'assigned_to': 'maria_design', 'priority': 'high', 'status': 'in_progress',
            'due_date': date.today() + timedelta(days=5)
        },
        {
            'title': 'Бэкенд разработка API',
            'description': 'Реализовать REST API для аутентификации, управления пользователями и документами.',
            'project': 0, 'assigned_to': 'alex_dev', 'priority': 'high', 'status': 'todo',
            'due_date': date.today() + timedelta(days=10)
        },
        {
            'title': 'Тестирование безопасности',
            'description': 'Провести пентест и аудит безопасности системы.',
            'project': 0, 'assigned_to': 'john_qa', 'priority': 'medium', 'status': 'review',
            'due_date': date.today() + timedelta(days=15)
        },
        
        # Проект 2: Мобильное приложение
        {
            'title': 'Прототипирование экранов',
            'description': 'Создать интерактивные прототипы основных экранов приложения.',
            'project': 1, 'assigned_to': 'maria_design', 'priority': 'medium', 'status': 'done',
            'due_date': date.today() - timedelta(days=2)
        },
        {
            'title': 'iOS разработка',
            'description': 'Нативная реализация приложения для iOS на Swift.',
            'project': 1, 'assigned_to': 'alex_dev', 'priority': 'high', 'status': 'in_progress',
            'due_date': date.today() + timedelta(days=7)
        },
        {
            'title': 'Тестирование на реальных устройствах',
            'description': 'Тестирование приложения на различных iOS и Android устройствах.',
            'project': 1, 'assigned_to': 'john_qa', 'priority': 'medium', 'status': 'todo',
            'due_date': date.today() + timedelta(days=12)
        },
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        assigned_user = User.objects.get(username=task_data['assigned_to'])
        
        task, created = Task.objects.get_or_create(
            title=task_data['title'],
            project=projects[task_data['project']],
            defaults={
                'description': task_data['description'],
                'assigned_to': assigned_user,
                'priority': task_data['priority'],
                'status': task_data['status'],
                'due_date': task_data.get('due_date'),
                'created_by': users['manager']
            }
        )
        if created:
            created_tasks.append(task)
            print(f"   ✅ Создана задача: {task.title} → {assigned_user.username}")
        else:
            created_tasks.append(task)
            print(f"   ⚠️ Задача уже существует: {task.title}")
    
    return created_tasks

def create_demo_comments(tasks, users):
    """Создание демонстрационных комментариев"""
    print("\n💬 Создание демонстрационных комментариев...")
    
    comments_data = [
        {
            'task': 0,  # Дизайн интерфейса
            'author': 'maria_design',
            'content': 'Начала работу над дизайном. Есть вопросы по цветовой схеме - нужно уточнить корпоративные цвета.'
        },
        {
            'task': 0,
            'author': 'manager_demo', 
            'content': 'Используйте цвета из нашего брендбука: синий #1E40AF и серый #6B7280'
        },
        {
            'task': 1,  # Бэкенд API
            'author': 'alex_dev',
            'content': 'API готов на 70%. Осталось реализовать эндпоинты для загрузки файлов.'
        },
        {
            'task': 4,  # iOS разработка
            'author': 'alex_dev',
            'content': 'Столкнулся с проблемой совместимости с iOS 14. Нужно дополнительное время для решения.'
        },
    ]
    
    for comment_data in comments_data:
        author = User.objects.get(username=comment_data['author'])
        
        comment, created = Comment.objects.get_or_create(
            task=tasks[comment_data['task']],
            author=author,
            content=comment_data['content']
        )
        if created:
            print(f"   ✅ Комментарий от {author.username}")
        else:
            print(f"   ⚠️ Комментарий уже существует")

def main():
    """Основная функция настройки демо-данных"""
    print("🎪 НАСТРОЙКА ДЕМОНСТРАЦИОННЫХ ДАННЫХ PROJECTFLOW")
    print("=" * 60)
    
    try:
        # Создаем пользователей
        users = create_demo_users()
        
        # Создаем проекты
        projects = create_demo_projects(users['manager'])
        
        # Создаем задачи
        tasks = create_demo_tasks(projects, users)
        
        # Создаем комментарии
        create_demo_comments(tasks, users)
        
        print("\n" + "=" * 60)
        print("🎉 ДЕМОНСТРАЦИОННЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ!")
        print("=" * 60)
        
        # Показываем информацию для доступа
        print("\n🔐 ДЕМО-ДОСТУПЫ:")
        print("   Администратор: admin_demo / admin123")
        print("   Менеджер: manager_demo / manager123") 
        print("   Разработчик: alex_dev / user123")
        print("   Дизайнер: maria_design / user123")
        print("   Тестировщик: john_qa / user123")
        
        print("\n🌐 ДЛЯ ДЕМОНСТРАЦИИ:")
        print("   1. Зайдите под разными пользователями")
        print("   2. Проверьте разные уровни доступа")
        print("   3. Попробуйте завершить задачи")
        print("   4. Протестируйте создание комментариев")
        
        print("\n🚀 Запустите сервер: python manage.py runserver")
        
    except Exception as e:
        print(f"❌ Ошибка при создании демо-данных: {e}")

if __name__ == '__main__':
    main()