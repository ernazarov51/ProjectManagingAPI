from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import Project, User, Sprint, Task, AssignHistory
from apps.serializers import ProjectModelSerializer, UserRegisterModelSerializer, SprintModelSerializer, \
    TaskModelSerializer, AssignSerializer, AssignHistoryModelSerializer, SprintModelSerializerr


# Create your views here.
@extend_schema(tags=['auth'])
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterModelSerializer
    queryset = User.objects.all()


@extend_schema(tags=['auth'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['auth'])
class CustomTokenRefreshView(TokenRefreshView):
    pass


class ProjectModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_destroy(self, instance):
        if instance.created_by != self.request.user:
            raise PermissionDenied("You are not owner this project")

        instance.delete()


@extend_schema(tags=['projects'])
class MyProjectsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(sprints__tasks__user=self.request.user)

@extend_schema(tags=['projects'])
class ProjectsByMeListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class SprintModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sprint.objects.all()
    serializer_class = SprintModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SprintByProjectListAPIView(ListAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintModelSerializerr

    def get_queryset(self):
        qs=super().get_queryset()
        project_id=self.kwargs.get('project_id')
        return qs.filter(project_id=project_id)





class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TaskModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



@extend_schema(tags=['tasks'], request=AssignSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_assign(request):
    print(request.data)














