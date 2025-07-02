from rest_framework.routers import DefaultRouter
from .views import SubjectListCreateAPIView, SubjectDetailAPIView, CourseListCreateAPIView, CourseDetailAPIView, CommentViewSet, RatingViewSet 
from django.urls import path, include

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    # path('subjects/',SubjectList.as_view()),
    # path('subjects/create/',SubjectCreate.as_view()),
    # path('subjects/<int:pk>',SubjectDetail.as_view()),
    # path('subjects/update/<int:pk>',SubjectUpdate.as_view()),
    # path('subjects/delete/<int:pk>',SubjectDelete.as_view()),
    # path('course_list/',CourseList.as_view()),
    # path('course/<int:pk>', CourseDetail.as_view()),
    # path('course/create/',CourseCreate.as_view()),
    # path('course/update/<int:pk>', CourseUpdate.as_view()),
    # path('course/delete/<int:pk>', CourseDelete.as_view()),
    path('subjects/',SubjectListCreateAPIView.as_view()),
    path('subjects/<int:subject_id>',SubjectDetailAPIView.as_view()),
    path('course_list/',CourseListCreateAPIView.as_view()),
    path('course_detail/<int:course_id>',CourseDetailAPIView.as_view()),

    path('', include(router.urls)),
]
