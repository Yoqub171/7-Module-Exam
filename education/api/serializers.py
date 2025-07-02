from rest_framework import serializers
from ..models import Subject, Course, Comment, Rating

class CourseModelSerializers(serializers.ModelSerializer):
    subject_title = serializers.StringRelatedField(source='subject.title')
    subject_slug = serializers.SlugRelatedField(
        source = 'subject',
        slug_field = 'slug',
        read_only = True
    )  
    username = serializers.CharField(source = 'owner.email')
    
    
    class Meta:
        model = Course
        fields = '__all__'


class SubjectModelSerializers(serializers.ModelSerializer):
    courses = CourseModelSerializers(many = True, read_only=True)
    course_count = serializers.SerializerMethodField()

    def get_course_count(self, obj):
        return obj.courses.count()

    class Meta:
        model = Subject
        fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'course', 'text', 'created_at']


class RatingSerializers(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'course', 'value']