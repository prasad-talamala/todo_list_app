from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.utils import timezone

from todo_app.forms import SignUpForm, ChangePasswordForm, CreateTodoForm
from todo_app.models import Todo


def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    user_obj = User.objects.get(id=request.user.id)
    if request.method == "GET":
        return render(request, 'profile.html', {'user_data': user_obj})
    else:
        if request.POST["first_name"]:
            user_obj.first_name = request.POST["first_name"]
        if request.POST["last_name"]:
            user_obj.last_name = request.POST["last_name"]
        if request.POST["email"]:
            user_obj.email = request.POST["email"]
        user_obj.save()
        messages.success(request, "Profile Updated Successfully.")
        return render(request, 'profile.html', {'user_data': user_obj})


def signup(request):
    if request.user.is_authenticated:
        return redirect('todos')
    else:
        if request.method == "GET":
            form = SignUpForm()
            return render(request, "signup.html", {"form": form})
        else:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                    email=request.POST['email'],
                                                    first_name=request.POST['first_name'],
                                                    last_name=request.POST['last_name'])
                    user.save()
                    return redirect("login")
                except IntegrityError:
                    messages.error(request, "username already taken..")
                    return render(request, "register.html", {"form": SignUpForm()})
            else:
                messages.error(request, "The two password fields didn't match.")
                return render(request, "register.html", {"form": SignUpForm()})


def login(request):
    if request.user.is_authenticated:
        return redirect('todos')
    else:
        if request.method == "GET":
            form = AuthenticationForm()
            return render(request, "login.html", {"form": form})
        else:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                messages.error(request, "username and password didn't match")
                return render(request, "login.html", {"form": AuthenticationForm()})
            else:
                auth_login(request, user)
                return redirect("todos")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")


@login_required
def change_password(request):
    if request.method == "GET":
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {"form": form})
    else:
        if request.POST['new_password'] == request.POST['confirm_new_password']:
            user = authenticate(request, username=request.user.username, password=request.POST["old_password"])
            if user is None:
                messages.error(request, "old password is wrong.")
                return render(request, "change_password.html", {"form": ChangePasswordForm()})
            else:
                user.set_password(request.POST['new_password'])
                user.save()
                messages.error(request, "password changed successfully.")
                return redirect("login")
        else:
            messages.error(request, "The two new password fields didn't match.")
            return render(request, "change_password.html", {"form": ChangePasswordForm()})


@login_required
def todos(request):
    return render(request, 'todos.html')


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=True)
    return render(request, 'current_todos.html', {"todos": todos})


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, completed__isnull=False).order_by("-completed")
    return render(request, 'completed_todos.html', {"todos": todos})


@login_required
def create_todo(request):
    if request.method == "GET":
        form = CreateTodoForm()
        return render(request, 'create_todo.html', {"form": form})
    else:
        form = CreateTodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        messages.success(request, "todo created successfully.")
        return redirect("current_todos")


@login_required
def view_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == "GET":
        form = CreateTodoForm(instance=todo)
        return render(request, 'view_todo.html', {"todo": todo, "form": form})
    else:
        form = CreateTodoForm(request.POST, instance=todo)
        form.save()
        messages.success(request, "todo updated successfully.")
        return redirect("current_todos")


@login_required
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == "POST":
        todo.completed = timezone.now()
        todo.save()
        messages.success(request, "todo marked as completed.")
        return redirect("completed_todos")


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == "POST":
        todo.delete()
        messages.success(request, "todo deleted successfully.")
        return redirect("completed_todos")
