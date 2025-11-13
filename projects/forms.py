from django import forms
from .models import Project, Task, Comment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название проекта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите проект...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Название проекта',
            'description': 'Описание',
            'status': 'Статус',
        }
        help_texts = {
            'title': 'Укажите краткое и понятное название проекта',
            'description': 'Подробно опишите цели и задачи проекта',
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'assigned_to', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите задачу...'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'project': 'Проект',
            'assigned_to': 'Исполнитель',
            'priority': 'Приоритет',
            'status': 'Статус',
            'due_date': 'Срок выполнения',
        }
        help_texts = {
            'title': 'Краткое и понятное название задачи',
            'description': 'Подробное описание того, что нужно сделать',
            'due_date': 'Дата, к которой задача должна быть выполнена',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Можно ограничить список пользователей только обычными пользователями
        # self.fields['assigned_to'].queryset = User.objects.filter(userprofile__role='user')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите ваш комментарий...'}),
        }
        labels = {
            'content': 'Комментарий',
        }