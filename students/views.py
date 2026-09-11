from django.shortcuts import render

def student_list(request):
    return render(request, 'students/student_list.html')