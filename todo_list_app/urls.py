"""todo_list_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URL's
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("change_password/", views.change_password, name="change_password"),

    # Todo URL's
    path('', views.home, name="home"),
    path('todos', views.todos, name="todos"),
    path('current_todos', views.current_todos, name="current_todos"),
    path('completed_todos', views.completed_todos, name="completed_todos"),
    path('create_todo', views.create_todo, name="create_todo"),
    path('todo/<int:todo_id>', views.view_todo, name="view_todo"),
    path('todo/<int:todo_id>/complete', views.complete_todo, name="complete_todo"),
    path('todo/<int:todo_id>/delete_todo', views.delete_todo, name="delete_todo"),

]
