from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.TodoListApiView.as_view()),
    path('api/<str:username>/', views.TodoUserApiView.as_view()),
    path('api/<str:username>/<int:todo_id>/', views.TodoDetailApiView.as_view()),
]
