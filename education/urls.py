from django.urls import path
from .views import IndexView, AboutView, TeacherListView, CourseView, CoursesView
from .api_views import UserInfo,SubjectList,SubjectDetail,SubjectCreate, SubjectUpdate, SubjectDelete, CourseList, CourseDetail, CourseCreate, CourseUpdate, CourseDelete
app_name = 'education'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseView.as_view(), name='course_detail'),
    path('users/',UserInfo.as_view(),),
    path('subjects/',SubjectList.as_view()),
    path('subjects/create/',SubjectCreate.as_view()),
    path('subjects/<int:pk>',SubjectDetail.as_view()),
    path('subjects/update/<int:pk>',SubjectUpdate.as_view()),
    path('subjects/delete/<int:pk>',SubjectDelete.as_view()),
    path('course_list/',CourseList.as_view()),
    path('course/<int:pk>', CourseDetail.as_view()),
    path('course/create/',CourseCreate.as_view()),
    path('course/update/<int:pk>', CourseUpdate.as_view()),
    path('course/delete/<int:pk>', CourseDelete.as_view()),
    
]
