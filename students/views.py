
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .models import Student



def student_list(request):
    students = Student.objects.all()
    return render(
        request,
        'students/student_list.html',
        {'students': students}
    )


# Add student to database
def student_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']

        Student.objects.create(
            name=name,
            email=email,
            age=age
        )

        return redirect('student_list')

    return render(request, 'students/student_form.html')



#  user registration
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'students/register.html')

# user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('student_list')

    return render(request, 'students/login.html')

# user logout
def logout_view(request):
    logout(request)
    return redirect('login')