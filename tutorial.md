# TodoAPI Tutorials

## Setup

Follow the "Environment Setup" section in the README for instructions on how to set up Python and Django.

## Models

First, we need to create a model for a todo item. All models are defined in `todo/models.py`. The following is an example of what the Todo model should look like:

```python
from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=200)
    completed = models.BooleanField(null=True, default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Now in order for Django to update the project to use our new model, we need to run **migrations**. Migrations are what take our models and build database tables for them. Instructions for how to update the database are also included in the README, but I've added them below for convenience.

> ### Updating the database
> 
> If you ever make changes to the models in a project, you will need to update the database, by migrating the changes. To do this, run:
> ```sh
> py manage.py makemigrations todo
> py manage.py migrate
> ```
> 
> The first command saves the model changes made in the todo project, and the second command applies these changes.

Now that we've applied the changes, we can start up our server and play around with what we have. Since we haven't set up any views yet, we'll use the interactive Python shell.

```python
# Start the interactive shell.
py manage.py shell

# We need to import the model that we created.
>>> from todo.models import Todo

# Query for all Todo items. We haven't made any yet, so it should be empty.
>>> Todo.objects.all()
<QuerySet []>

# Let's make a Todo item! First we need to get access to a user to assign the Todo to.
>>> from django.contrib.auth.models import User
>>> admin = User.objects.get(username='admin')
# Now we can make the Todo item!
>>> task = Todo(task="Finish demo", completed=False, user=admin)
>>> task.save()

# If we query for all Todo items, we get something now!
>>> Todo.objects.all()
<QuerySet [<Todo: Todo object (1)>]>

# Exit the interactive shell.
>>> exit()
```

If you check in the database and refresh it, there should now be an entry in the todo_todo table with the Todo object we just made.

The information that was printed to the console when we ran `Todo.objects.all()` the second time wasn't very useful, so let's work on improving it. All we need to do is add a `__str__()` method to the Todo model class to tell it what to print to the console. Here's an example of what that might look like:

```py
class Todo(models.Model):

    # other code omitted...

    def __str__(self):
        return self.task
```

Now, lets try listing the Todo objects in the database again.

```python
# Start the interactive shell.
py manage.py shell

# We need to import the model that we created.
>>> from todo.models import Todo

# Query for all Todo items. The result should be a little more descriptive this time
>>> Todo.objects.all()
<QuerySet [<Todo: Finish demo>]>

# Exit the interactive shell.
>>> exit()
```

## Django Admin Panel
Although playing with the API through the Python shell is fun, it's not at all practical. Thankfully, Django provides an admin panel with minimal setup. If you look in `mysite/urls.py`, you'll find some URL paths that I already set up. It should look like the following:

```python
from django.contrib import admin
from django.urls import include, path
from todo import urls as todo_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('todo/', include(todo_urls)),
]
```

The `admin/` URL path is assigned to `admin.site.urls`. If you start up the server and navigate to http://127.0.0.1:8000/admin/, you'll be prompted for a username and password. On this admin panel, you can modify the groups and users stored in the database.

So how do we interact with the Todo model? We need to register the Todo model with the admin site. In `todo/admin.py`, add the following code:

```python
from . import models

admin.site.register(models.Todo)
```

Now if you refresh the admin panel, you should see a new section for the Todo model! Open the Todo model page by clicking on "Todo" and select the Todo item we created previously. You can edit the task, for example, set completed to "Yes". If you save the change and open the database in VS Code (make sure to refresh the database), you can see the changes you made! Also notice that `updated` field was automatically changed to the datetime of when you saved the changes.

One last thing before we continue, let's make a second user in the admin panel for later use. Click "Home" in the top left, select "Add" next to the Users section, and fill out the form. For the sake of consistency, I'd suggest setting the username and password to `bob`. Don't forget to save the new user before closing the admin panel.

## Views

Using the admin panel is great, but we don't want everyone to have admin access. This is where we begin building the actual API part of the backend. Our goal is to create a collection of API **endpoints** that allow users to access (or modify) specific information. Endpoints are just the URLs we use to grant access to the information. For example, http://127.0.0.1:8000/api/admin/1/ would be the path to access the Todo object we created. First, we need to create a serializer for the object. Serializers tell Django how to translate between Python objects and JSON. In `todo/serializers.py`, add the following code:

```python
from . import models

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = ["id", "task", "completed", "user", "created", "updated"]
```

It's okay if this looks a little strange. What you should focus on is that the serializer is using the Todo model. The fields array specifies which fields should be included in the JSON object, or in other words, which fields should be made visible to the user.

### GET View

Next, we need to make a view. The first view we will make will return a list of all the Todo objects. In `todo/views.py`, add the following code:

```python
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
```

Each APIView has a name (TodoListApiView, in this case) and optionally defines one or more HTTP methods, such as GET, POST, PUT, and DELETE (we are only defining GET). In the `get()` method, you can see we are using the same `Todo.objects.all()` call that we used in the Python shell to access all the Todo objects. Before we can send the data to the user though, we have to serialize it, or turn it into JSON, so that the user can read it. We pass the list of todo objects to the TodoSerializer, tell the serializer that there are multiple objects, and then return an HTTP Response object with the data from the serializer.

Finally, we need to assign the view to a URL endpoint. All we need to do is add an entry to the `urlpatterns` array in `todo/urls.py` like the following:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.TodoListApiView.as_view()),
]
```

Now if you navigate to http://127.0.0.1:8000/todo/api/, you should see a list of all the Todo items currently in the database!

> ### Exploring `mysite/urls.py`
> You might ask why we have to add `todo/` to the URL. If you look in `mysite/urls.py`, you'll see that we are importing the urls from `todo/urls.py` and assigning them to the `todo/` path. So when we put the full path together, we have `todo/` + `api/` to get `todo/api/`.
>
> ```python
> from django.contrib import admin
> from django.urls import include, path
> from todo import urls as todo_urls
>
> urlpatterns = [
>     path('admin/', admin.site.urls),
>     path('auth/', include('rest_framework.urls')),
>     path('todo/', include(todo_urls)),
> ]
> ```
>
> You'll also notice that we have an `auth/` path. That path would be used for user authentication to make sure they have permissions to view or modify the data they are requesting, but we have all authentication disabled in this demo project, so we won't be using it.

### POST View

Now that we've set up our first API to get all the Todo objects, let's make an API so that we can create new Todo objects! We can reuse the same serializer class, so we just need to make a new view. This view will allow us to look at specific users and create new Todo items for a user. Here's an example of what that might look like:

```python
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
```

The above view has two different HTTP methods, GET and POST. The GET method returns all the Todo objects for a given user. We accomplish this by filtering for Todos by the user's ID. The POST method takes the data provided by the user and creates a new Todo object using the TodoSerializer again. You'll notice that both methods have a `username` parameter. This parameter will hold the username of the user we want to get information about.

Now let's update the URL paths to include this new view:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.TodoListApiView.as_view()),
    path('api/<str:username>/', views.TodoUserApiView.as_view()),
]
```

This path looks a little strange compared to the first one. The `<str:username>` part of the URL acts a lot like a variable. For example, if we navigate to `api/admin/`, Django matches "admin" to the `username` variable in the URL and will send that parameter to the GET and POST methods.

If we navigate to this endpoint, http://127.0.0.1:8000/todo/api/admin/, it'll look a little different than the last one. That is because unlike the other endpoint, we can POST data to create new Todo items. We can use the "Content" field to create a Todo item in JSON format:

```json
{
    "task": "Make a new task"    
}
```

Nice and simple! Notice that we didn't set the `completed` and `user` fields like we did previously. The `completed` field is marked as optional in the Todo model (`blank=true`) and defaults to false if left empty (`default=False`). When we click the "POST" button at the bottom, we'll get an "HTTP 201 Created" response, and the new Todo item will be returned to us with all the other fields filled in. Either refesh the page or click the "GET" button to see all the Todo items that the admin user now owns.

### PATCH and DELETE View

Okay, we have one more view to create. We still need some way to edit or delete existing Todo items. The following view supports both of these operations:

```python
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
```

It may look like a lot, but this view is following the same basic structure as the previous two. Each method now has two additional parameters, `username` and `todo_id`. Like before, these will be defined in the URL path. The GET method now filters by username and Todo id, so it'll only return one object. The PATCH method finds an existing Todo object and combines the original data with the new data using the TodoSerializer. The DELETE method simply removes the item from the database.

Once again, we need to add the URL to our list of paths:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.TodoListApiView.as_view()),
    path('api/<str:username>/', views.TodoUserApiView.as_view()),
    path('api/<str:username>/<int:todo_id>/', views.TodoDetailApiView.as_view()),
]
```

You can see the two variables that we are are using in the HTTP methods in the URL path again.

## Conclusion

At this point, you should have a fully functional Todo list API! You can create, read, update, and delete Todo items using the three endpoints we made. Feel free to play around with what you have to learn more about Django and APIs. You could try adding a new view, changing the structure of our URL paths, or even creating a new model to store some new data!