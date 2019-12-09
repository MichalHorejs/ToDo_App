from django.shortcuts import render, redirect
from .models import User, Task


def home_view(request):
    return load_page(request, 'home.html')


def about_view(request):
    return load_page(request, 'about.html')


def register_view(request):
    return render(request, 'register.html')


def login_view(request):
    content = {
        'success': ''
    }
    try:
        content['success'] = request.session['success']
        del request.session['success']
        return render(request, 'login.html', content)

    except KeyError:
        return render(request, 'login.html')


def add_task(request):
    return load_page(request, 'add.html')


# authenticate if both passwords are the same
def register_authentication(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_again = request.POST.get('password_again')

    content = {
        'state': '',
    }

    try:
        user = User.objects.get(username=username)
        content['state'] = 'User already exists '
        return render(request, 'register.html', content)

    except User.DoesNotExist:
        if password != password_again:
            content['state'] = 'Your passwords doesn\'t match '
            return render(request, 'register.html', content)

        # save data into database
        else:
            content['state'] = 'Registration was successful ! \n Now log in.'

            user = User(username=username, password=password)
            user.save()

            request.session['success'] = content['state']

            return redirect(login_view)


# authenticate users login
def login_authentication(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    content = {
        'state': '',
    }

    try:
        user = User.objects.get(username=username)

        if password == user.password:
            request.session['login'] = True
            request.session['user'] = user.username
            return redirect(home_view)
        else:
            content['state'] = 'Wrong username or password !'
            return render(request, 'login.html', content)

    except User.DoesNotExist:
        content['state'] = 'Wrong username or password !'
        return render(request, 'login.html', content)


def logout(request):
    del request.session['login']
    del request.session['user']
    return redirect(home_view)


def load_page(request, page_name):
    content = {
        'logged': False,
        'user': '',
        'tasks': '',
    }

    try:
        if request.session['login']:
            content['logged'] = True
            content['user'] = request.session['user']

            if page_name == 'home.html':
                user = User.objects.get(username=content['user'])
                tasks = user.task_set.all()
                content['tasks'] = tasks

        return render(request, page_name, content)
    except KeyError:
        return render(request, page_name)


def save_task(request):
    new_task = request.POST.get('task')

    user = User.objects.get(username=request.session['user'])
    task = Task(task=new_task, user=user)
    task.save()

    return redirect(home_view)


def remove_task(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(pk=task_id)
    task.delete()

    return redirect(home_view)
