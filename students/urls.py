from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),

    # URL for user registration
    path('register/', views.register, name='register'),
    # URL for user login
    path('login/', views.login_view, name='login'),
    # URL for user logout
    path('logout/', views.logout_view, name='logout'),
    # URL for student form
    path('add/', views.student_form, name='student_form'),

]