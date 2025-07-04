from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer, AssignSerializer
from .models import Task
from .permissions import IsOwnerOrReadOnly, IsOwnerOrAssignedTo
from accounts.models import MyUser

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def list(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        serializer = UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        team = get_object_or_404(Task, pk=pk)
        serializer = UpdateTaskSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post']) 
    def assignToUser(self, request, pk, user_id):
        serializer = AssignSerializer(data = request.data)
        task = get_object_or_404(Task, pk=pk)
        user = get_object_or_404(MyUser, pk = user_id)
        if task.team not in user.teams.all():
            return Response({'detail': 'User is not part of the task\'s team.'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            task.assigned_to = user
            task.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unassignToUser(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.assigned_to = ''
        task.save()
        return Response('Unassigned successfully!')