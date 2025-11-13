#!/usr/bin/env python
"""
Скрипт для запуска всех тестов проекта ProjectFlow
"""

import os
import django

def run_tests():
    """Запуск всех тестов проекта"""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project_manager.settings'
    django.setup()
    
    print("=" * 70)
    print("ЗАПУСК ТЕСТОВ PROJECTFLOW")
    print("=" * 70)
    
    # Запускаем тесты с помощью manage.py
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'accounts', 'projects', 'api', '--verbosity=2'])

if __name__ == '__main__':
    run_tests()