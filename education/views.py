from django.shortcuts import render, get_object_or_404
from .models import Subject, Course, Teacher
# Create your views here.

def index(request):
    search_query = request.GET.get('q', '')
    subject_id = request.GET.get('subject')

    popular_courses = Course.objects.all()[:6]

    subjects = Subject.objects.all()

    if subject_id:
        courses = Course.objects.filter(subject_id=subject_id)
    elif search_query:
        courses = Course.objects.filter(title__icontains=search_query)
    else:
        courses = Course.objects.all()


    context = {
        'subjects': subjects,
        'courses': courses,
        'search_query': search_query,
        'selected_subject_id': subject_id,
        'popular_courses': popular_courses,
    }

    return render(request, 'education/index.html', context)


def about_view(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()

    return render(request, 'education/about.html', {'subjects': subjects, 'courses': courses})

def teachers_view(request):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'education/teacher.html', {
        'teachers': teachers,
        'subjects': subjects
    })

def courses_view(request):
    courses = Course.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'education/course.html', {
        'courses': courses,
        'subjects': subjects
    })


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'education/course_detail.html', {'course': course})