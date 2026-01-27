from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.models import Project, User, Sprint, Task, AssignHistory


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'created_by': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        project = Project.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.created_by != user:
            raise serializers.ValidationError({'msg': 'You are not owner this project'}, 400)
        instance = super().update(instance, validated_data)
        return instance


class UserRegisterModelSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value: str):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['password']:
            raise serializers.ValidationError('Passwords not match', 400)
        attrs['password'] = make_password(attrs['password'])
        return attrs

    def create(self, validated_data: dict):
        validated_data.pop('confirm_password')
        return User.objects.create(**validated_data)


class SprintModelSerializer(ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True}
        }


    def update(self, instance: Sprint, validated_data):
        user = self.context['request'].user
        if instance.project.created_by != user:
            raise serializers.ValidationError('This project not yours')
        instance = super().update(instance, validated_data)
        return instance

    def create(self, validated_data):
        user = self.context['request'].user
        project = validated_data['project']
        if user.id!=project.created_by.id:
            raise serializers.ValidationError("This project not yours")
        sprint=Sprint.objects.create(**validated_data)
        return sprint

class SprintModelSerializerr(ModelSerializer):
    class Meta:
        model=Sprint
        fields='__all__'


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'
        extra_kwargs={
            'status':{'read_only':True},
            'created_at':{'read_only':True}
        }

    def update(self, instance:Task, validated_data):
        user=self.context['request'].user
        if instance.sprint.project.created_by!=user:
            raise serializers.ValidationError('This action is not allowed for you',400)

        instance=super().update(instance,validated_data)
        return instance

class AssignSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    reason = serializers.CharField(max_length=500)

class AssignHistoryModelSerializer(ModelSerializer):
    class Meta:
        model = AssignHistory
        fields = '__all__'

class UserListModelSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email']




