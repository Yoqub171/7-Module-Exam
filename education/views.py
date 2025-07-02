from django.shortcuts import render, get_object_or_404
from .models import Subject, Course, Teacher, Comment
from django.db.models import Avg
from django.views.generic import ListView, TemplateView, DetailView

# def index(request):
#     search_query = request.GET.get('q', '')
#     subject_id = request.GET.get('subject')

#     popular_courses = Course.objects.all()[:6]

#     teachers = Teacher.objects.all()

#     subjects = Subject.objects.all()

#     if subject_id:
#         courses = Course.objects.filter(subject_id=subject_id)
#     elif search_query:
#         courses = Course.objects.filter(title__icontains=search_query)
#     else:
#         courses = Course.objects.all()


#     context = {
#         'subjects': subjects,
#         'courses': courses,
#         'search_query': search_query,
#         'selected_subject_id': subject_id,
#         'popular_courses': popular_courses,
#         'teachers': teachers,
#     }

#     return render(request, 'education/index.html', context)


class IndexView(TemplateView):
    template_name = 'education/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subject_id = self.request.GET.get('subject')
        search_query = self.request.GET.get('q', '')

        if subject_id:
            courses = Course.objects.filter(subject_id=subject_id)
        elif search_query:
            courses = Course.objects.filter(title__icontains=search_query)
        else:
            courses = Course.objects.all()

        context['subjects'] = Subject.objects.all()
        context['courses'] = courses
        context['search_query'] = search_query
        context['selected_subject_id'] = subject_id
        context['popular_courses'] = Course.objects.all()[:6]
        context['teachers'] = Teacher.objects.all()
        
        return context
    


# def about_view(request):
#     subjects = Subject.objects.all()
#     courses = Course.objects.all()

#     return render(request, 'education/about.html', {'subjects': subjects, 'courses': courses})


class AboutView(TemplateView):
    template_name = 'education/about.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['courses'] = Course.objects.all()
        return context


class TeacherListView(ListView):
    model = Teacher
    template_name = 'education/teacher.html'
    context_object_name  = 'teachers'

    def get_queryset(self):
        return Teacher.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['courses'] = Course.objects.all()
        return context

# def courses_view(request):
#     courses = Course.objects.all()
#     subjects = Subject.objects.all()
#     return render(request, 'education/course.html', {
#         'courses': courses,
#         'subjects': subjects
#     })


class CourseView(ListView):
    model = Course
    template_name = 'education/course.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['popular_courses'] = Course.objects.order_by('-id')[:6]
        return context


# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     teacher = getattr(course.owner, 'teacher_profile', None)

#     context = {
#         'course': course,
#         'teacher': teacher,
#     }

#     return render(request, 'education/course_detail.html', context)


class CourseDetail(DetailView):
    model = Course
    template_name = 'education/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        teacher = getattr(course.owner, 'teacher_profile', None)
        context['teacher'] = teacher

        comments = Comment.objects.filter(course=course)
        avg_rating = course.ratings.aggregate(avg=Avg('value'))['avg'] or 0

        context['comments'] = comments
        context['avg_rating'] = round(avg_rating, 1)

        return context