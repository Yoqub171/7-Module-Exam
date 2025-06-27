from django.urls import path
from .views import index, about_view, teachers_view, course_detail, courses_view

app_name = 'education'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about_view, name='about'),
    path('teachers/', teachers_view, name='teachers'),
    path('courses/', courses_view, name='courses'),
    path('courses/<int:pk>/', course_detail, name='course_detail'),
]
