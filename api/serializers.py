from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from projects.models import Project, Task, Comment

class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['role', 'role_display', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'project_title',
            'assigned_to', 'assigned_to_name', 'priority', 'status',
            'due_date', 'created_by', 'created_by_name', 'created_at',
            'updated_at', 'comments'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'status', 'created_by',
            'created_by_name', 'created_at', 'updated_at', 'tasks',
            'tasks_count'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='user')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs
    
    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        # Обновляем роль пользователя
        user_profile = user.userprofile
        user_profile.role = role
        user_profile.save()
        
        return user