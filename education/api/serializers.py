from rest_framework import serializers
from ..models import Subject, Course, Comment, Rating
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


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

    

class CustomTokenObtainPairSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        data['full_name'] = self.user.full_name
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['created_at'] = datetime.now()

        return data
    

class LogoutSerizlizer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('Token is invalid or expired  ')