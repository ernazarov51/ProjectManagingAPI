from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.models import Project, User, Sprint, Task, AssignHistory
from apps.serializers import ProjectModelSerializer, UserRegisterModelSerializer, SprintModelSerializer, \
    TaskModelSerializer, AssignSerializer, AssignHistoryModelSerializer, SprintModelSerializerr, \
    UserListModelSerializer, UserUpdateModelSerializer, UserForgotPasswordModelSerializer


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
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class SprintModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Sprint.objects.all()
    serializer_class = SprintModelSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_destroy(self, instance):
        if instance.project.created_by != self.request.user:
            raise PermissionDenied("You are not owner this project")

        instance.delete()


@extend_schema(tags=['sprints'])
class SprintByProjectListAPIView(ListAPIView):
    queryset = Sprint.objects.all()
    serializer_class = SprintModelSerializerr

    def get_queryset(self):
        qs = super().get_queryset()
        project_id = self.kwargs.get('project_id')
        return qs.filter(project_id=project_id)


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TaskModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema(tags=['tasks'],
               parameters=[
                   OpenApiParameter(name='state', description='project yoki sprint', required=True, type=str),
                   OpenApiParameter(name='id', description='Project yoki Sprint ID', required=True, type=int),
               ]
               )
class TaskBySprintListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        state = self.request.GET.get('state')
        id = self.request.GET.get('id')
        states = ['project', 'sprint']
        if state not in states:
            print(True)
            return ValidationError("This state is not found", 400)
        if state == 'project':
            qs.filter(sprint__project_id=id)
            return qs
        return qs.filter(sprint_id=id)


@extend_schema(tags=['assign history'])
class AssignHistoryListAPIView(ListAPIView):
    queryset = AssignHistory.objects.all()
    serializer_class = AssignHistoryModelSerializer

    def get_queryset(self):
        qs=super().get_queryset()
        return qs.filter(task_id=self.kwargs.get('task_id'))


@extend_schema(tags=['assign history'], request=AssignSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def task_assign(request, task_id):
    if not task_id:
        raise ValidationError("task_id must be sent", 400)
    task = Task.objects.filter(id=task_id)
    if not task:
        raise ValidationError("Task Not Found")
    task = task.first()
    user = User.objects.filter(id=request.data.get('user_id'))
    if not user:
        raise ValidationError("user not Found")
    user = user.first()
    if task.user == user:
        raise ValidationError(f"anyway, this task belongs to the {user.username}")
    if user == request.user:
        raise ValidationError(f"this task belongs to you")
    task.user = user
    task.save()
    serializer = TaskModelSerializer(instance=task)
    reason = request.data.get('reason')
    channel_layer = get_channel_layer()

    assign_history = AssignHistory.objects.create(reason=reason, task=task, old_worker=request.user, new_worker=user)
    async_to_sync(channel_layer.group_send)(
        f"user_{task.user.id}",
        {
            "type": "send_notification",
            "data": {
                "type": "AssignTask",
                "message": f"{request.user.username} assigned his own task to you",
                "task": dict(serializer.data),
                "reason": reason,
                "time": f"{assign_history.created_at}"
            }
        }
    )
    return JsonResponse(serializer.data)


@extend_schema(tags=['user'])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListModelSerializer


@extend_schema(tags=['user'])
class UserDetailRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(id=self.kwargs.get('pk'))
@extend_schema(tags=['user'])
class UserModelUpdateAPIView(UpdateAPIView):
    permission_classes([IsAuthenticated])
    serializer_class = UserUpdateModelSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        c=super().get_serializer_context()
        c['user']=self.request.user
        return c

@extend_schema(tags=['user'],request=UserForgotPasswordModelSerializer)
@api_view(['POST'])
def forgot_password(request):
    if request.method=='POST':
        user=request.user
        serializer=UserForgotPasswordModelSerializer(data=request.data,context={'user':user})
        if serializer.is_valid():
            print(True)
            serializer.save()
            return JsonResponse(serializer.data)
        print(False)
        return JsonResponse(serializer.errors)
class WSTemplateView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        token = self.kwargs.get('token')
        context['token'] = token
        return context



