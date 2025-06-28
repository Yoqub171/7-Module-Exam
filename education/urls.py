from django.urls import path
from .views import IndexView, AboutView, TeacherListView, CourseView, CoursesView

app_name = 'education'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseView.as_view(), name='course_detail'),
]
