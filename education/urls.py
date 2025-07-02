from django.urls import path
from django.urls import include
from .views import IndexView, AboutView, TeacherListView, CourseView, CourseDetail
app_name = 'education'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
    path('', include('education.api.urls')),

]
