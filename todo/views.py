from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from django.contrib.auth.models import User

class TodoListApiView(APIView):

    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(instance=todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TodoUserApiView(APIView):

    def get_user_id(self, username):
        user = User.objects.get(username=username)
        return user.id

    def get(self, request, username):
        todos = Todo.objects.filter(user=self.get_user_id(username))
        serializer = TodoSerializer(instance=todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username):
        data = request.data
        data['user'] = self.get_user_id(username)

        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailApiView(APIView):

    def get_object(self, username, todo_id):
        user = User.objects.get(username=username)
        return Todo.objects.get(id=todo_id, user=user.id)

    def get(self, request, username, todo_id):
        todo_instance = self.get_object(username, todo_id)
        serializer = TodoSerializer(instance=todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, username, todo_id):
        todo_instance = self.get_object(username, todo_id)
        serializer = TodoSerializer(instance=todo_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username, todo_id):
        todo_instance = self.get_object(username, todo_id)
        todo_instance.delete()
        return Response(status=status.HTTP_200_OK)
