from django.contrib import admin
from django.urls import include, path
from todo import urls as todo_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('todo/', include(todo_urls)),
]
