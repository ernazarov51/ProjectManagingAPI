from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProjectModelViewSet, UserCreateAPIView, MyProjectsAPIView, SprintModelViewSet, TaskModelViewSet, \
    ProjectsByMeListAPIView, task_assign, SprintByProjectListAPIView

router = DefaultRouter()
router.register('projects', ProjectModelViewSet)
router.register('sprints', SprintModelViewSet)
router.register('tasks', TaskModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('my-projects/', MyProjectsAPIView.as_view(), name='my-projects'),
    path('projects-by-me/', ProjectsByMeListAPIView.as_view(), name='projects-by-me'),
    path('assign/', task_assign, name='projects-by-me'),
    path('sprintss/<int:project_id>/',SprintByProjectListAPIView.as_view()),
    path('register/', UserCreateAPIView.as_view(), name='register')
]
