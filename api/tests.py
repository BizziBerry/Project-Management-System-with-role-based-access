from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from projects.models import Project, Task
from accounts.models import UserProfile

class APIAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.admin = User.objects.create_user('admin', 'admin123')
        admin_profile = UserProfile.objects.get(user=self.admin)
        admin_profile.role = 'admin'
        admin_profile.save()
        
        self.manager = User.objects.create_user('manager', 'manager123')
        manager_profile = UserProfile.objects.get(user=self.manager)
        manager_profile.role = 'manager'
        manager_profile.save()
        
        self.user = User.objects.create_user('user', 'user123')

    def test_api_registration(self):
        """Тест регистрации через API"""
        response = self.client.post('/api/auth/register/', {
            'username': 'newapiuser',
            'email': 'api@test.com',
            'password': 'apipassword123',
            'password_confirm': 'apipassword123',
            'role': 'user'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newapiuser').exists())

    def test_api_projects_access(self):
        """Тест доступа к проектам через API"""
        # Неавторизованный доступ - 403 Forbidden (из-за IsAuthenticated permission)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Авторизованный доступ
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class APIRoleBasedTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
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
        
        self.task_user1 = Task.objects.create(
            title='Task for User1',
            project=self.project,
            assigned_to=self.user1,
            created_by=self.manager
        )
        
        self.task_user2 = Task.objects.create(
            title='Task for User2', 
            project=self.project,
            assigned_to=self.user2,
            created_by=self.manager
        )

    def test_user_task_visibility(self):
        """Тест видимости задач для пользователей через API"""
        # User1 должен видеть только свои задачи
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверяем, что в ответе есть только задачи user1
        tasks_data = response.json()
        tasks = tasks_data.get('results', []) if 'results' in tasks_data else tasks_data
        
        # Должна быть только одна задача - та, что назначена на user1
        user1_tasks = [task for task in tasks if task['assigned_to'] == self.user1.id]
        self.assertEqual(len(user1_tasks), 1)
        self.assertEqual(user1_tasks[0]['title'], 'Task for User1')