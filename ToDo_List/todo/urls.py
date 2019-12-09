from django.contrib import admin
from django.urls import path
from .views import home_view, about_view, register_view, login_view, register_authentication, login_authentication, \
    logout, add_task, save_task, remove_task

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),
    path('about/', about_view, name="about"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('register_authentication', register_authentication, name="register_authentication"),
    path('login_authentication', login_authentication, name='login_authentication'),
    path('logout/', logout, name='logout'),
    path('add/', add_task, name='add_task'),
    path('save_task', save_task, name='save_task'),
    path('remove_task', remove_task, name='remove_task'),
]
