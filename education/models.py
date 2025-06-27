from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title
    
class Course(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True,blank=True)
    duration = models.TimeField()
    price = models.DecimalField(max_digits=14,decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL ,related_name='user_courses', on_delete=models.SET_NULL,null=True,blank=True)
    image = models.ImageField(upload_to='course/images')
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='courses')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title   
    

class ItemBase(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Text(ItemBase):
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Video(ItemBase):
    url = models.URLField()

    def __str__(self):
        return self.title

class Image(ItemBase):
    image = models.FileField()

    def __str__(self):
        return self.title

class File(ItemBase):
    file = models.FileField()

    def __str__(self):
        return self.title


class Topic(models.Model):
    module = models.ForeignKey(Module,
                               related_name='topics',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to= {'model__in':(
                                         'text',
                                         'video',
                                         'image',
                                         'file',
                                     )}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    my_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['my_order']
   


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name