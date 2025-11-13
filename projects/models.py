from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date

class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('on_hold', 'На паузе'),
    ]
    
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'))
    status = models.CharField(_('Статус'), max_length=10, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects', verbose_name=_('Создатель'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')
        permissions = [
            ("can_delete_project", "Can delete project"),
        ]

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]
    
    STATUS_CHOICES = [
        ('todo', 'К выполнению'),
        ('in_progress', 'В работе'),
        ('review', 'На проверке'),
        ('done', 'Выполнено'),
    ]
    
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name=_('Проект'))
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name=_('Исполнитель'))
    priority = models.CharField(_('Приоритет'), max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(_('Статус'), max_length=15, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(_('Срок выполнения'), null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name=_('Создатель'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.project.title}"
    
    def is_overdue(self):
        """Проверяет, просрочена ли задача"""
        if self.due_date and self.status != 'done':
            return self.due_date < date.today()
        return False
    
    def can_user_complete(self, user):
        """Проверяет, может ли пользователь завершить задачу"""
        return (
            user.is_authenticated and 
            self.assigned_to == user and 
            self.status != 'done'
        )
    
    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Задача'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    content = models.TextField(_('Содержание'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    def __str__(self):
        return f"Комментарий от {self.author.username} к задаче {self.task.title}"
    
    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')