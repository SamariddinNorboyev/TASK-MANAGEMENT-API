from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status as http_status
from .models import Task
from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer
from .models import Task
from .permissions import IsOwnerOrAssignedTo
from accounts.models import MyUser

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrAssignedTo]

    def list(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = self.get_object()
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateTaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        task = self.get_object()
        serializer = UpdateTaskSerializer(instance = task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        task = self.get_object()
        serializer = UpdateTaskSerializer(instance = task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = self.get_object()
        task.delete()
        return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post']) 
    def assignToUser(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        user_id = request.data.get('user_id')
        user = get_object_or_404(MyUser, pk = user_id)
        if task.team not in user.teams.all():
            return Response({'detail': 'User is not part of the task\'s team.'}, status=status.HTTP_400_BAD_REQUEST)
        task.assigned_to = user
        task.save()
        seriazlier = TaskSerializer(task)
        return Response(seriazlier.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def unassignToUser(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.assigned_to = None
        task.save()
        seriazlier = TaskSerializer(task)
        return Response(seriazlier.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        task = self.get_object()
        user = request.user
        new_status = request.data.get('status')

        if new_status not in Task.Status.values:
            return Response({"detail": "Invalid status value."}, status=http_status.HTTP_400_BAD_REQUEST)

        current = task.status

        if user == task.assigned_to:
            if current == Task.Status.TODO and new_status == Task.Status.INPROGRESS:
                task.status = new_status
                task.save()
                return Response({"detail": "Status updated to In Progress."})
            elif current == Task.Status.INPROGRESS and new_status == Task.Status.INREVIEW:
                task.status = new_status
                task.save()
                return Response({"detail": "Status updated to In Review."})
            else:
                return Response({"detail": "You cannot change the status at this stage."},
                                status=http_status.HTTP_403_FORBIDDEN)

        elif user == task.team.owner:
            if current == Task.Status.INREVIEW and new_status in [
                Task.Status.DONE,
                Task.Status.TODO,
                Task.Status.INREVIEW,
            ]:
                task.status = new_status
                task.save()
                return Response({"detail": f"Status updated to {new_status}."})
            else:
                return Response({"detail": "As owner, you can only change status from INREVIEW."},
                                status=http_status.HTTP_403_FORBIDDEN)

        return Response({"detail": "You are not allowed to change the task status."},
                        status=http_status.HTTP_403_FORBIDDEN)