from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course, Comment, Rating
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from .serializers import SubjectModelSerializers, CourseModelSerializers, CommentSerializers, RatingSerializers
from django.db.models import Avg, Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
    

# class SubjectList(APIView):
#     def get(self, request):
#         subjects = Subject.objects.all().order_by('id')
#         serializers = SubjectModelSerializers(subjects, many=True)
#         return Response(serializers.data, status=HTTP_200_OK)
    

# class SubjectDetail(APIView):
#     def get(self, request, pk):
#         try:
#             subject = Subject.objects.get(id =pk)
#             serializers = SubjectModelSerializers(subject)
#             return Response(serializers.data, status=HTTP_200_OK)
#         except Subject.DoesNotExist:
#             subject = None
#             data = {
#                 'status' :HTTP_404_NOT_FOUND,
#                 'message': 'Subject Not Found'
#             }
#         return Response(data)


# class SubjectCreate(APIView):
#     def post(self,request):
#         serializer = SubjectModelSerializers(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(f"{serializer.data['title']} successfully created",status=HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

# class SubjectUpdate(APIView):
#     def post(self, request, pk):
#         try:
#             subject = Subject.objects.get(pk = pk)
#         except Subject.DoesNotExist:
#             return Response({"error": "Subject not found"}, status=HTTP_404_NOT_FOUND)
        
#         serializer = SubjectModelSerializers(subject, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Subject successfully updated", "data": serializer.data}, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_404_NOT_FOUND)
    

# class SubjectDelete(APIView):
#     def get(self, request, pk):
#         try:
#             subject = Subject.objects.get(pk=pk)
#         except Subject.DoesNotExist:
#             return Response({"error": "Subject not found"}, status=HTTP_404_NOT_FOUND)
        
#         subject.delete()
#         return Response({"message": "Subject successfully deleted"}, status=HTTP_200_OK)




# class CourseList(APIView):
#     def get(self, request):
#         courses = Course.objects.all().order_by('id')
#         serializer = CoursetModelSerializers(courses, many=True)
#         return Response(serializer.data, status=HTTP_200_OK)

# class CourseDetail(APIView):
#     def get(self, request, pk):
#         try:
#             course = Course.objects.get(pk=pk)
#             serializer = CoursetModelSerializers(course)
#             return Response(serializer.data, status=HTTP_200_OK)
#         except Course.DoesNotExist:
#             subject = None
#             data = {
#                 'status': HTTP_404_NOT_FOUND,
#                 'message': 'Course not found',
#             }
#         return Response(data)
    

        
# class CourseCreate(APIView):
#     def post(self, request):
#         serializer = CoursetModelSerializers(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(f"{serializer.data['titlt']} successfully created", status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    


# class CourseUpdate(APIView):
#     def post(self, request, pk):
#         try:
#             course = Course.objects.get(pk=pk)
#         except Subject.DoesNotExist:
#             return Response({"error": "Course npt found"}, status=HTTP_404_NOT_FOUND)
        
#         serializer = CoursetModelSerializers(course, data=request.data)
#         if serializer.is_valid():
#             return Response({"message": "Course successfully updated", "data": serializer.data}, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_404_NOT_FOUND)


# class CourseDelete(APIView):
#     def get(self, request, pk):
#         try:
#             course = Course.objects.get(pk=pk)
#         except Course.DoesNotExist:
#             return Response({"error": "Course not found"}, status=HTTP_404_NOT_FOUND)
        
#         course.delete()
#         return Response({"message": "Subject successfully created"}, status=HTTP_200_OK)


class SubjectListCreateAPIView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializers
    
    def get_queryset(self):
        queryset = Subject.objects.all()
        queryset = queryset.annotate(course_count=Count('courses'))
        queryset = queryset.order_by('course_count')
        return queryset
    
    
class SubjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializers
    lookup_url_kwarg = 'subject_id'


class CourseListCreateAPIView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializers

    def get_queryset(self):
        queryset = Course.objects.all().order_by('-id')
        return queryset
    

class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all().annotate(avg_rating = Avg('ratings__value'))
    serializer_class = CourseModelSerializers
    lookup_url_kwarg = 'course_id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)

        comments = Comment.objects.filter(course = instance)
        comments_data = CommentSerializers(comments, many=True).data

        return Response({
            **serializers.data,
            'average_rating': instance.avg_rating or 0,
            'comments': comments_data
        })


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        existing_rating = Rating.objects.filter(user=self.request.user, course=course).first()
        if existing_rating:
            existing_rating.value = serializer.validated_data['value']
            existing_rating.save()
        else:
            serializer.save(user=self.request.user)

        