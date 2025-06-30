
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subject, Course
from rest_framework.status import HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_201_CREATED,HTTP_400_BAD_REQUEST
from .serializers import SubjectModelSerializers, CoursetModelSerializers


class UserInfo(APIView):
    def get(self, request):
        user_data = {
            1:{
                'name': 'Iphone 16',
                'description': 'asdfwef',
                'price': 1234,
                'image': 'htpps://www.com',
                'category': 'Apple',
            }
        }

        return Response(user_data)
    

class SubjectList(APIView):
    def get(self, request):
        subjects = Subject.objects.all().order_by('id')
        serializers = SubjectModelSerializers(subjects, many=True)
        return Response(serializers.data, status=HTTP_200_OK)
    

class SubjectDetail(APIView):
    def get(self, request, pk):
        try:
            subject = Subject.objects.get(id =pk)
            serializers = SubjectModelSerializers(subject)
            return Response(serializers.data, status=HTTP_200_OK)
        except Subject.DoesNotExist:
            subject = None
            data = {
                'status' :HTTP_404_NOT_FOUND,
                'message': 'Subject Not Found'
            }
        return Response(data)


class SubjectCreate(APIView):
    def post(self,request):
        serializer = SubjectModelSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"{serializer.data['title']} successfully created",status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class SubjectUpdate(APIView):
    def post(self, request, pk):
        try:
            subject = Subject.objects.get(pk = pk)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=HTTP_404_NOT_FOUND)
        
        serializer = SubjectModelSerializers(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Subject successfully updated", "data": serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_404_NOT_FOUND)
    

class SubjectDelete(APIView):
    def get(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=HTTP_404_NOT_FOUND)
        
        subject.delete()
        return Response({"message": "Subject successfully deleted"}, status=HTTP_200_OK)




class CourseList(APIView):
    def get(self, request):
        courses = Course.objects.all().order_by('id')
        serializer = CoursetModelSerializers(courses, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class CourseDetail(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            serializer = CoursetModelSerializers(course)
            return Response(serializer.data, status=HTTP_200_OK)
        except Course.DoesNotExist:
            subject = None
            data = {
                'status': HTTP_404_NOT_FOUND,
                'message': 'Course not found',
            }
        return Response(data)
    

        
class CourseCreate(APIView):
    def post(self, request):
        serializer = CoursetModelSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f"{serializer.data['titlt']} successfully created", status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    


class CourseUpdate(APIView):
    def post(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({"error": "Course npt found"}, status=HTTP_404_NOT_FOUND)
        
        serializer = CoursetModelSerializers(course, data=request.data)
        if serializer.is_valid():
            return Response({"message": "Course successfully updated", "data": serializer.data}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_404_NOT_FOUND)


class CourseDelete(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=HTTP_404_NOT_FOUND)
        
        course.delete()
        return Response({"message": "Subject successfully created"}, status=HTTP_200_OK)