from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from education.models import (
    Subject, Course, Module, Text, Video, Image, File, Topic, Teacher, Comment, Rating
)
from users.models import CustomUser

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

class ModuleResource(resources.ModelResource):
    class Meta:
        model = Module

class TextResource(resources.ModelResource):
    class Meta:
        model = Text

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

class ImageResource(resources.ModelResource):
    class Meta:
        model = Image

class FileResource(resources.ModelResource):
    class Meta:
        model = File

class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher

class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ('id', 'title', 'slug')

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ('id', 'title', 'subject', 'price', 'duration', 'owner')

@admin.register(Module)
class ModuleAdmin(ImportExportModelAdmin):
    resource_class = ModuleResource
    list_display = ('id', 'title', 'course')

@admin.register(Text)
class TextAdmin(ImportExportModelAdmin):
    resource_class = TextResource
    list_display = ('id', 'title', 'created_at', 'updated_at')

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_class = VideoResource
    list_display = ('id', 'title', 'url', 'created_at')

@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    resource_class = ImageResource
    list_display = ('id', 'title', 'image', 'created_at')

@admin.register(File)
class FileAdmin(ImportExportModelAdmin):
    resource_class = FileResource
    list_display = ('id', 'title', 'file', 'created_at')

@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    resource_class = TopicResource
    list_display = ('id', 'module', 'content_type', 'object_id', 'my_order')

@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    resource_class = TeacherResource
    list_display = ('id', 'user', 'full_name', 'position')

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    resource_class = CustomUserResource
    list_display = ('id', 'full_name', 'email', 'is_teacher', 'is_staff', 'joined')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'text', 'created_at']
    search_fields = ['text', 'user__username', 'course__title']
    list_filter = ['created_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'value']
    list_filter = ['value']
    search_fields = ['user__username', 'course__title']