
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import Student
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def student_list(request):
    students = Student.objects.all()

    search = request.GET.get('search')

    if search:
        students = students.filter(name__icontains=search)

    total_students = students.count()

    return render(
        request,
        'students/student_list.html',
        {
            'students': students,
            'total_students': total_students
        }
    )


@login_required
def student_form(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        course = request.POST.get('course')

        errors = []

        # Name validation
        if not name:
            errors.append("Name is required.")

        # Email validation
        if not email:
            errors.append("Email is required.")

        # Age validation
        if not age:
            errors.append("Age is required.")
        else:
            try:
                age = int(age)

                if age < 1 or age > 100:
                    errors.append("Age must be between 1 and 100.")

            except ValueError:
                errors.append("Age must be a valid number.")

        # Course validation
        if not course:
            errors.append("Course is required.")

        # If errors exist
        if errors:
            return render(
                request,
                'students/student_form.html',
                {
                    'errors': errors,
                    'name': name,
                    'email': email,
                    'age': age,
                    'course': course
                }
            )

        # Save student
        Student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )

        # Go back to student list
        return redirect('student_list')

    return render(request, 'students/student_form.html')

# Edit student details

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email'].lower()
        student.age = request.POST['age']
        student.course = request.POST['course']
        student.save()

        return redirect('student_list')

    return render(
        request,
        'students/edit_student.html',
        {'student': student}
    )

# Delete student
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()

    return redirect('student_list')

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