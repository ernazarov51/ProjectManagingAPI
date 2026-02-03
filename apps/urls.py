from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import ProjectModelViewSet, UserCreateAPIView, MyProjectsAPIView, SprintModelViewSet, TaskModelViewSet, \
    ProjectsByMeListAPIView, task_assign, SprintByProjectListAPIView, AssignHistoryListAPIView, UserListAPIView, \
    TaskBySprintListAPIView, UserDetailRetrieveAPIView, WSTemplateView, UserModelUpdateAPIView, forgot_password

router = DefaultRouter()
router.register('projects', ProjectModelViewSet)
router.register('sprints', SprintModelViewSet)
router.register('tasks', TaskModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('my-projects/', MyProjectsAPIView.as_view(), name='my-projects'),
    path('projects-by-me/', ProjectsByMeListAPIView.as_view(), name='projects-by-me'),
    path('assign/<int:task_id>/', task_assign),
    path('assign-history/<int:task_id>/', AssignHistoryListAPIView.as_view()),
    path('sprintss/<int:project_id>/',SprintByProjectListAPIView.as_view()),
    path('tasks-special/',TaskBySprintListAPIView.as_view()),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('all-users/',UserListAPIView.as_view()),
    path('user-detail/<int:pk>/',UserDetailRetrieveAPIView.as_view()),
    path('user-update/<int:pk>/',UserModelUpdateAPIView.as_view()),
    path('forgot-password/',forgot_password),
    path('connect/<str:token>/',WSTemplateView.as_view()),
]
