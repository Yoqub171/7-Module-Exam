from rest_framework import serializers
from .models import Subject, Course

class SubjectModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subject
        # fields = '__all__'
        exclude = ('slug',)


class CoursetModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
