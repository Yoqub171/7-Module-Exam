from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject, Course, Comment, Rating
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED, HTTP_204_NO_CONTENT
)
from .serializers import SubjectModelSerializers, CourseModelSerializers, CommentSerializers, RatingSerializers, LogoutSerizlizer
from django.db.models import Avg, Count
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import (
    MondayFriday,
    IsOwnerOrReadOnly,
    JohnReadOnly,
    IsJohnBlocked,
    CanReadPremiumCourse,
    IsEvenYear,
    LoginOnlySuperUser,
    PutPatchOnly
)
from .tokens import get_or_create_token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializers


User = get_user_model()


    

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.all().order_by('-id')
        return queryset
    

class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all().annotate(avg_rating = Avg('ratings__value'))
    serializer_class = CourseModelSerializers
    lookup_url_kwarg = 'course_id'
    permission_classes = [IsAuthenticated]

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

        
class PremiumCourse(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializers
    permission_classes = [CanReadPremiumCourse, IsEvenYear]

    def get_queryset(self):
        return Course.objects.filter(is_premium = True)


class RegsiterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        full_name = request.data.get("full_name")
        password = request.data.get("password")

        if not email or not password or not full_name:
            return Response({"error": "Email, full_name va password kerak"}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, full_name=full_name, password=password)
        token = get_or_create_token(user)
        return Response({"token": token}, status=HTTP_201_CREATED)
    

class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=HTTP_401_UNAUTHORIZED)

        token = get_or_create_token(user)
        return Response({"token": token}, status=HTTP_200_OK)
    

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerizlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Successfully logged out"}, status=HTTP_204_NO_CONTENT)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializers