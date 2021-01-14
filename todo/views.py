from collections import OrderedDict
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions 
from rest_framework import status
from rest_framework.response import Response
from todo.permissions import IsTodoListOwner, IsOwner
from todo.serializers import TodoSerializer, TodoListSerializer, RegisterSerializer
from todo.models import TodoList, Todo


# Create your views here.
class TodoLists(generics.ListCreateAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(owner=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TodoListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

class Todos(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = TodoList.objects.all()
    lookup_url_kwarg = 'list_pk'

    permission_classes = [
        permissions.IsAuthenticated, 
        IsTodoListOwner,
    ]

    def list(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        todo_list = TodoList.objects.get(pk=list_pk)
        
        queryset = todo_list.todos.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 

    def create(self, request, *args, **kwargs):
        # Get todo list ID from URL
        list_pk = kwargs['list_pk']

        try:
            TodoList.objects.get(pk=list_pk)
        except:
            raise exceptions.NotFound(
                detail='Todo list not found')
        
        # Clone request.data and add todo list ID
        todo = OrderedDict()
        todo.update(request.data)
        todo['todo_list'] = list_pk

        serializer = self.get_serializer(data=todo)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def retrieve(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        todo_pk = kwargs['pk']

        todo_list = TodoList.objects.get(pk=list_pk)
        queryset = todo_list.todos.get(pk=todo_pk)

        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data) 

    def update(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        todo_pk = kwargs['pk']
        partial = kwargs.pop('partial', False)

        todo = Todo.objects.get(id=todo_pk, todo_list=list_pk)
        serializer = self.get_serializer(instance=todo, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data) 

    def destroy(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        todo_pk = kwargs['pk']

        todo = Todo.objects.get(id=todo_pk, todo_list=list_pk)
        self.perform_destroy(todo)

        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
    serializer_class = RegisterSerializer




