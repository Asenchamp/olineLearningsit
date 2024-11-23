from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name='base'

urlpatterns = [
  path('',views.about, name="about"),
  path('/courses',views.courses, name="courses"),
  path('/contact',views.contact, name="contact"),
  path('course/',views.course, name="course"),
  path('instructors/',views.instructors, name="instructors"),
  path('topic/<int:course_id>/',views.topic, name="topic"),
  path('Courseadmin/<str:instructor_id>/',views.Courseadmin, name="Courseadmin"),
  path('notes/<int:topic_id>/',views.notes, name="notes"),
  path('createnotes/<str:instructor_id>/',views.createnotes,name="createnotes"),
  path('updatenotes/<str:instructor_id>/<int:topic_id>/',views.updatenotes,name="updatenotes"),
  path('deletenotes/<str:instructor_id>/<int:topic_id>/',views.deletenotes,name="deletenotes"),
  path('deletemessage/<int:course_id>/<int:cohort_id>/<int:message_id>/<str:Id>/',views.deletemessage,name="deletemessage"),
  path('cohort/<int:cohort_id>/<int:course_id>/<str:Id>/',views.cohort,name="cohort"),
  path('setexercise/<str:instructor_id>/<int:topic_id>/',views.setexercise,name="setexercise"),
  path('exercise/<str:user_id>/<int:topic_id>/',views.exercise,name="exercise"),
  path('deleteexercise/<str:id>/<int:topic_id>/<int:exercise_id>/',views.deleteexercise,name="deleteexercise"),
  path('mark/<str:student_id>/<int:topic_id>/<int:exercise_id>/',views.mark,name="mark"),
  path('changepassword/<str:userid>/', views.changepassword, name='changepassword'),
  path('send_reset_email/<str:userid>/', views.send_reset_email_to_user, name='send_reset_email_to_user'),
  path('send_email/<str:userid>/', views.send_email, name='send_email'),
  path('resetpassword/<str:userid>/', views.resetpassword, name='resetpassword'),
  path('login/', views.login_view, name='login'),
  path('post/create/', views.create_post, name='create_post'),
  path('post/', views.post_detail, name='post'),
  path('post/<int:post_id>/', views.like_post, name='like_post'),
  path('admindashboard/<int:userid>/', views.user_view, name='user_view'),
  path('deletepost/<int:post_id>/<int:Id>/', views.deletepost, name='deletepost'),  
]


