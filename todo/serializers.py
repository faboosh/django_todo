from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from todo.models import Todo, TodoList

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = [
            'id', 
            'title', 
            'created_at', 
            'is_completed', 
            'todo_list',
        ]

    def to_representation(self, obj):
        representation = super(TodoSerializer, self).to_representation(obj)

        representation.pop('todo_list')

        return representation 

class TodoListSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)
    class Meta:
        model = TodoList
        fields = [
            'id', 
            'title', 
            'created_at', 
            'todos',
        ]

class UserSerializer(serializers.ModelSerializer):
    todo_lists = serializers.PrimaryKeyRelatedField(many=True, queryset=TodoList.objects.all())

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'todo_lists'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
                required=True,
                validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(
                write_only=True, 
                required=True, 
                validators=[validate_password]
            )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user
