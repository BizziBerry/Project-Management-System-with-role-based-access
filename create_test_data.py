import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import Project, Task, Comment
from accounts.models import UserProfile

def create_test_users():
    print("Создание тестовых пользователей...")
    
    # Создаем менеджера
    if not User.objects.filter(username='manager').exists():
        manager_user = User.objects.create_user('manager', 'manager@example.com', 'manager123')
        manager_user.save()
        manager_profile, created = UserProfile.objects.get_or_create(user=manager_user)
        manager_profile.role = 'manager'
        manager_profile.save()
        print("✅ Менеджер создан: manager / manager123")
    else:
        print("⚠ Менеджер уже существует")
    
    # Создаем обычных пользователей
    test_users = [
        ('user1', 'user1@example.com', 'user123'),
        ('user2', 'user2@example.com', 'user123'),
        ('user3', 'user3@example.com', 'user123'),
    ]
    
    for username, email, password in test_users:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            user.save()
            print(f"✅ Пользователь создан: {username} / {password}")
        else:
            print(f"⚠ Пользователь {username} уже существует")

def create_test_projects():
    print("\nСоздание тестовых проектов...")
    
    manager_user = User.objects.get(username='manager')
    
    projects_data = [
        {
            'title': 'Разработка веб-сайта компании',
            'description': 'Создание современного корпоративного веб-сайта с системой управления контентом и адаптивным дизайном',
            'status': 'active'
        },
        {
            'title': 'Мобильное приложение для заказов',
            'description': 'Разработка кроссплатформенного мобильного приложения для iOS и Android с системой онлайн-заказов',
            'status': 'active'
        },
        {
            'title': 'Внутренняя система аналитики',
            'description': 'Система для автоматизации сбора, анализа и визуализации бизнес-метрик и KPI',
            'status': 'on_hold'
        },
        {
            'title': 'Обновление CRM системы',
            'description': 'Модернизация и расширение функционала существующей CRM системы',
            'status': 'completed'
        }
    ]
    
    for project_data in projects_data:
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults={
                'description': project_data['description'],
                'status': project_data['status'],
                'created_by': manager_user
            }
        )
        if created:
            print(f"✅ Проект создан: {project.title}")
        else:
            print(f"⚠ Проект уже существует: {project.title}")

def create_test_tasks():
    print("\nСоздание тестовых задач...")
    
    manager_user = User.objects.get(username='manager')
    user1 = User.objects.get(username='user1')
    user2 = User.objects.get(username='user2')
    user3 = User.objects.get(username='user3')
    
    website_project = Project.objects.get(title='Разработка веб-сайта компании')
    mobile_project = Project.objects.get(title='Мобильное приложение для заказов')
    analytics_project = Project.objects.get(title='Внутренняя система аналитики')
    
    tasks_data = [
        # Задачи для веб-сайта
        {
            'title': 'Дизайн пользовательского интерфейса',
            'description': 'Разработка UI/UX дизайна для всех страниц сайта с учетом современных тенденций',
            'project': website_project,
            'assigned_to': user1,
            'priority': 'high',
            'status': 'in_progress'
        },
        {
            'title': 'Фронтенд разработка',
            'description': 'Верстка и реализация клиентской части на React.js',
            'project': website_project,
            'assigned_to': user2,
            'priority': 'high',
            'status': 'todo'
        },
        {
            'title': 'Бэкенд API',
            'description': 'Разработка REST API для взаимодействия с фронтендом',
            'project': website_project,
            'assigned_to': user3,
            'priority': 'medium',
            'status': 'todo'
        },
        
        # Задачи для мобильного приложения
        {
            'title': 'Прототипирование приложения',
            'description': 'Создание интерактивных прототипов основных экранов приложения',
            'project': mobile_project,
            'assigned_to': user1,
            'priority': 'medium',
            'status': 'review'
        },
        {
            'title': 'Разработка iOS версии',
            'description': 'Нативная разработка приложения для iOS на Swift',
            'project': mobile_project,
            'assigned_to': user2,
            'priority': 'high',
            'status': 'in_progress'
        },
    ]
    
    for task_data in tasks_data:
        task, created = Task.objects.get_or_create(
            title=task_data['title'],
            project=task_data['project'],
            defaults={
                'description': task_data['description'],
                'assigned_to': task_data['assigned_to'],
                'priority': task_data['priority'],
                'status': task_data['status'],
                'created_by': manager_user
            }
        )
        if created:
            print(f"✅ Задача создана: {task.title}")

def main():
    print("=== СОЗДАНИЕ ТЕСТОВЫХ ДАННЫХ ===\n")
    
    create_test_users()
    create_test_projects()
    create_test_tasks()
    
    print("\n=== ТЕСТОВЫЕ ДАННЫЕ СОЗДАНЫ ===")
    print("\nДоступные пользователи:")
    print("👑 Администратор: admin / admin123")
    print("👔 Менеджер: manager / manager123") 
    print("👤 Пользователь 1: user1 / user123")
    print("👤 Пользователь 2: user2 / user123")
    print("👤 Пользователь 3: user3 / user123")
    
    print("\nАдмин-панель: http://127.0.0.1:8000/admin/")
    print("Главная страница: http://127.0.0.1:8000/")

if __name__ == '__main__':
    main()