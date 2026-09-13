
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import Student


# =========================
# Student List
# =========================

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


# =========================
# Add Student
# =========================
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

                if age < 1 or age > 50:
                    errors.append("Age must be between 1 and 50.")

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

        # Success message
        messages.success(
            request,
            'Student added successfully!'
        )

        # Go back to student list
        return redirect('student_list')

    # This is required when opening Add Student page
    return render(request, 'students/student_form.html')
# =========================
# Edit Student
# =========================

@login_required
def edit_student(request, id):

    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':

        student.name = request.POST['name']
        student.email = request.POST['email'].lower()
        student.age = request.POST['age']
        student.course = request.POST['course']

        student.save()

        messages.success(request, 'Student updated successfully!')

        return redirect('student_list')

    return render(
        request,
        'students/edit_student.html',
        {'student': student}
    )


# =========================
# Delete Student
# =========================

@login_required
def delete_student(request, id):

    student = get_object_or_404(Student, id=id)

    student.delete()

    messages.success(
        request,
        'Student deleted successfully!'
    )

    return redirect('student_list')

# =========================
# User Registration
# =========================

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Username already exists. Please choose another username.'
            )

            return redirect('register')

        # Create new user
        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(
            request,
            'Registration successful! Please login.'
        )

        return redirect('login')

    return render(request, 'students/register.html')


# =========================
# User Login
# =========================
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check whether username is registered
        if not User.objects.filter(username=username).exists():
            messages.error(
                request,
                'User not found. Please register first.'
            )
            return redirect('login')

        # Check username and password
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('student_list')

        else:
            messages.error(
                request,
                'Invalid password.'
            )

    return render(request, 'students/login.html')


def logout_view(request):
    list(messages.get_messages(request))
    logout(request)
    return redirect('login')