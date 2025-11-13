from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from projects.models import Project, Task, Comment
from .serializers import (
    UserSerializer, ProjectSerializer, TaskSerializer,
    CommentSerializer, UserRegistrationSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'userprofile'):
            if user.userprofile.is_admin() or user.userprofile.is_manager():
                return Project.objects.all()
        return Project.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_destroy(self, instance):
        if not self.request.user.userprofile.is_admin():
            raise permissions.PermissionDenied("Только администраторы могут удалять проекты")
        instance.delete()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'userprofile'):
            if user.userprofile.is_admin() or user.userprofile.is_manager():
                return Task.objects.all()
            else:
                return Task.objects.filter(assigned_to=user)
        return Task.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        user = request.user
        
        if hasattr(user, 'userprofile') and user.userprofile.is_user() and task.assigned_to != user:
            return Response(
                {"error": "Вы не можете завершить эту задачу"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        task.status = 'done'
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    return Response(
        {'error': 'Неверные учетные данные'},
        status=status.HTTP_400_BAD_REQUEST
    )