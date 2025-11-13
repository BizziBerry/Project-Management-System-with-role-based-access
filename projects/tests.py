from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project, Task, Comment
from accounts.models import UserProfile

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description', 
            created_by=self.user
        )

    def test_project_creation(self):
        """Тест создания проекта"""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.status, 'active')
        self.assertEqual(self.project.created_by, self.user)

    def test_project_str_method(self):
        """Тест строкового представления проекта"""
        self.assertEqual(str(self.project), 'Test Project')

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.assigned_user = User.objects.create_user(username='assigned_user', password='test123')
        self.project = Project.objects.create(
            title='Test Project',
            created_by=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Task Description',
            project=self.project,
            assigned_to=self.assigned_user,
            created_by=self.user
        )

    def test_task_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.assigned_user)

    def test_can_user_complete_method(self):
        """Тест метода проверки возможности завершения задачи"""
        # Назначенный пользователь может завершить незавершенную задачу
        self.assertTrue(self.task.can_user_complete(self.assigned_user))
        
        # Другой пользователь не может завершить задачу
        other_user = User.objects.create_user(username='other_user', password='test123')
        self.assertFalse(self.task.can_user_complete(other_user))

class ProjectAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Создаем пользователей с разными ролями
        self.admin = User.objects.create_user('admin', 'admin123')
        admin_profile = UserProfile.objects.get(user=self.admin)
        admin_profile.role = 'admin'
        admin_profile.save()
        
        self.manager = User.objects.create_user('manager', 'manager123') 
        manager_profile = UserProfile.objects.get(user=self.manager)
        manager_profile.role = 'manager'
        manager_profile.save()
        
        self.user = User.objects.create_user('user', 'user123')
        
        # Создаем тестовый проект
        self.project = Project.objects.create(
            title='Test Project',
            created_by=self.manager
        )

    def test_project_list_access(self):
        """Тест доступа к списку проектов"""
        # Неавторизованный пользователь - редирект на логин (302)
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 302)
        
        # Обычный пользователь - доступ разрешен (200)
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('project_list'))
        self.assertEqual(response.status_code, 200)

    def test_project_create_access(self):
        """Тест доступа к созданию проектов"""
        # Обычный пользователь не может создавать проекты - редирект (302)
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 302)
        
        # Менеджер может создавать проекты (200)
        self.client.login(username='manager', password='manager123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)
        
        # Администратор может создавать проекты (200)
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('project_create'))
        self.assertEqual(response.status_code, 200)

class TaskAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.manager = User.objects.create_user('manager', 'manager123')
        manager_profile = UserProfile.objects.get(user=self.manager)
        manager_profile.role = 'manager'
        manager_profile.save()
        
        self.user1 = User.objects.create_user('user1', 'user123')
        self.user2 = User.objects.create_user('user2', 'user123')
        
        self.project = Project.objects.create(
            title='Test Project', 
            created_by=self.manager
        )

    def test_task_completion_access(self):
        """Тест доступа к завершению задач"""
        # Создаем задачу для user1
        task = Task.objects.create(
            title='Test Task',
            project=self.project,
            assigned_to=self.user1,
            created_by=self.manager,
            status='todo'
        )
        
        # User1 может завершить свою задачу
        self.client.login(username='user1', password='user123')
        response = self.client.post(reverse('task_complete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        
        # Проверяем, что статус изменился
        task.refresh_from_db()
        self.assertEqual(task.status, 'done')