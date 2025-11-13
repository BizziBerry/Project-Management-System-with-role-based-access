from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile

class UserAuthenticationTests(TestCase):
    def setUp(self):
        """Создаем тестовых пользователей"""
        self.client = Client()
        
        # Создаем пользователей с разными ролями
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='admin123'
        )
        self.admin_profile = UserProfile.objects.get(user=self.admin_user)
        self.admin_profile.role = 'admin'
        self.admin_profile.save()
        
        self.manager_user = User.objects.create_user(
            username='manager_test', 
            password='manager123'
        )
        self.manager_profile = UserProfile.objects.get(user=self.manager_user)
        self.manager_profile.role = 'manager'
        self.manager_profile.save()
        
        self.regular_user = User.objects.create_user(
            username='user_test',
            password='user123'
        )

    def test_user_profile_creation(self):
        """Тест автоматического создания профиля при создании пользователя"""
        new_user = User.objects.create_user(
            username='new_user',
            password='test123'
        )
        self.assertTrue(hasattr(new_user, 'userprofile'))
        self.assertEqual(new_user.userprofile.role, 'user')

    def test_role_methods(self):
        """Тест методов проверки ролей"""
        self.assertTrue(self.admin_profile.is_admin())
        self.assertTrue(self.manager_profile.is_manager())
        self.assertTrue(self.regular_user.userprofile.is_user())

    def test_registration_page(self):
        """Тест доступности страницы регистрации"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

    def test_access_restrictions(self):
        """Тест ограничения доступа для неавторизованных пользователей"""
        protected_urls = [
            reverse('project_list'),
            reverse('profile'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)

class UserProfileTests(TestCase):
    def test_profile_str_method(self):
        """Тест строкового представления профиля"""
        user = User.objects.create_user(username='testuser', password='test123')
        profile = user.userprofile
        expected_str = f"{user.username} - {profile.get_role_display()}"
        self.assertEqual(str(profile), expected_str)