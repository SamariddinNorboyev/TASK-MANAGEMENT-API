from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Team
from .serializers import TeamSerializer, CreateTeamSerializer, UpdateTeamSerializer, AddOrRemoveMemberSerializer
from .permissions import IsOwnerOrReadOnly

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def create(self, request):
        serializer = CreateTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        serializer = UpdateTeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        serializer = UpdateTeamSerializer(team, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        team.delete()
        return Response({"detail": "Team deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        serializer = AddOrRemoveMemberSerializer(team, data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user_instance')
            team = Team.objects.get(pk=pk)
            team.members.add(user)
            return Response({'message': 'User added successfully'})

    @action(detail=True, methods=['post'])  
    def remove_user(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        serializer = AddOrRemoveMemberSerializer(team, data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user_instance')
            team = Team.objects.get(pk=pk)
            
            team.members.remove(user)
            return Response({'message': 'User removed successfully'})

    @action(detail=True, methods=['post'])    
    def remove_all_user(self, request, pk=None):
        team = self.get_object()
        # team = get_object_or_404(Team, pk=pk)
        team.members.clear()
        return Response({'message': 'Team is clear!'})
    

















    
# class TeamViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#     def list(self, request):
#         teams = Team.objects.all()
#         serializer = TeamSerializer(teams, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         team = get_object_or_404(Team, pk=pk)
#         serializer = TeamSerializer(team)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = CreateTeamSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk=None):
#         team = get_object_or_404(Team, pk=pk)
#         self.check_object_permissions(request, team)
#         serializer = UpdateTeamSerializer(team, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         self.check_object_permissions(request, team)
#         team = get_object_or_404(Team, pk=pk)
#         serializer = UpdateTeamSerializer(team, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         self.check_object_permissions(request, team)
#         team = get_object_or_404(Team, pk=pk)
#         team.delete()
#         return Response({"detail": "Team deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
#     @action(detail=True, methods=['post'])
#     def add_user(self, request, pk=None):
#         team = get_object_or_404(Team, pk=pk)
#         self.check_object_permissions(request, team)
#         serializer = AddOrRemoveMemberSerializer(team, data = request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data.get('user_instance')
#             team = Team.objects.get(pk=pk)
#             team.members.add(user)
#             return Response({'message': 'User added successfully'})

#     @action(detail=True, methods=['post'])  
#     def remove_user(self, request, pk=None):
#         team = get_object_or_404(Team, pk=pk)
#         self.check_object_permissions(request, team)
#         serializer = AddOrRemoveMemberSerializer(team, data = request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data.get('user_instance')
#             team = Team.objects.get(pk=pk)
#             team.members.remove(user)
#             return Response({'message': 'User removed successfully'})

#     @action(detail=True, methods=['post'])    
#     def remove_all_user(self, request, pk=None):
#         team = get_object_or_404(Team, pk=pk)
#         self.check_object_permissions(request, team)
#         team.members.clear()
#         return Response({'message': 'Team is clear!'})