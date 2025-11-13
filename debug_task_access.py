import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_manager.settings')
django.setup()

from django.contrib.auth.models import User
from projects.models import Task

def debug_task_access():
    print("=== ДИАГНОСТИКА ДОСТУПА К ЗАДАЧАМ ===\n")
    
    # Находим пользователя user1
    user = User.objects.get(username='user1')
    print(f"Тестируем пользователя: {user.username}")
    print(f"Роль пользователя: {user.userprofile.role}")
    print(f"ID пользователя: {user.id}\n")
    
    # Находим все задачи, назначенные на user1
    assigned_tasks = Task.objects.filter(assigned_to=user)
    print(f"Задач назначено на user1: {assigned_tasks.count()}")
    
    for task in assigned_tasks:
        print(f"\n--- Задача: {task.title} ---")
        print(f"ID задачи: {task.id}")
        print(f"Статус: {task.status}")
        print(f"Назначена на: {task.assigned_to.username} (ID: {task.assigned_to.id})")
        print(f"Создатель: {task.created_by.username}")
        
        # Проверяем условия для кнопки "Завершить"
        condition1 = task.assigned_to == user
        condition2 = task.status != 'done'
        
        print(f"Условие 1 (task.assigned_to == user): {condition1}")
        print(f"Условие 2 (task.status != 'done'): {condition2}")
        print(f"Показывать кнопку 'Завершить': {condition1 and condition2}")
        
        # Проверяем ID для точного сравнения
        print(f"ID assigned_to: {task.assigned_to.id}, ID user: {user.id}")
        print(f"ID равны: {task.assigned_to.id == user.id}")

if __name__ == '__main__':
    debug_task_access()