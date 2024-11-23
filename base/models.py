from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class Course(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name
  
class Cohort(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name
  
class School(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name
  
class Student(models.Model):
  name  = models.CharField(max_length=100)
  student_id = models.CharField(max_length=20,unique=True,blank=True,editable=False)
  student_image = models.ImageField(upload_to='students/')
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128,blank=True)
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
  cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True)
  school  = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
  score = models.IntegerField(default=0, editable=False)
  reset_pin = models.CharField(max_length=10, blank=True, null=True)

  def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

  def check_password(self, raw_password):
        return check_password(raw_password, self.password)
  
  def save(self, *args, **kwargs):
    if not self.student_id:
        prefix = "DIY-S-"
        unique_id = get_random_string(length=6, allowed_chars='0123456789')
        self.student_id = f"{prefix}{unique_id}"

    if not self.password:
        raw_password = get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.set_password(raw_password)

    super(Student, self).save(*args, **kwargs) 
  
  def __str__(self):
    return self.name

class Instructor(models.Model):
  name  = models.CharField(max_length=100)
  instructor_id = models.CharField(max_length=20,unique=True,blank=True,editable=False)
  instructor_image = models.ImageField(upload_to='instructors/')
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128,blank=True)
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
  school  = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
  reset_pin = models.CharField(max_length=10, blank=True, null=True)
  admin = models.CharField(max_length=100, default=False)

  def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

  def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
  def save(self, *args, **kwargs):
      if not self.instructor_id:
          prefix = "DIY-I-"
          unique_id = get_random_string(length=12, allowed_chars='0123456789')
          self.instructor_id = f"{prefix}{unique_id}"

      if not self.password:
          raw_password = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
          self.set_password(raw_password)

      super(Instructor, self).save(*args, **kwargs) 
    
  def __str__(self):
    return self.name

class Topic(models.Model):
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=200)
  description = models.CharField(max_length=25500)
  content = models.FileField(upload_to='notes/')
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.name

class Choice(models.Model):
  A = models.CharField(max_length=255)
  B = models.CharField(max_length=255)
  C = models.CharField(max_length=255)
  D = models.CharField(max_length=255)

  def __str__(self):
    return self.A

class Exercise(models.Model):
  Question = models.CharField(max_length=255)
  Answer = models.CharField(max_length=2)
  choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  message = models.CharField(max_length=255, default="null")
   
  def __str__(self):
    return self.Question
  
class Message(models.Model):
  cohort = models.ForeignKey(Cohort,on_delete=models.CASCADE)
  course = models.ForeignKey(Course,on_delete=models.CASCADE)
  user = models.CharField(max_length=40)
  body = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.body[0:50]
  
class StudentExerciseSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    message = models.CharField(max_length=255, default="null")

    def __str__ (self):
      return self.student

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption[:20]

class Media(models.Model):
    post = models.ForeignKey(Post, related_name='media', on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def media_type(self):
        if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return 'image'
        elif self.file.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            return 'video'
        return 'unknown'

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')







