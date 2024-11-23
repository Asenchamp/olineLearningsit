from django.shortcuts import render,redirect,reverse,get_object_or_404
from. import models, forms
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import PostForm, MediaFormSet
from .forms import LoginForm
from django.db.models import Q
# Create your views here.
def about(request):
  return render(request,'about.html')

def courses(request):
  return render(request,'courses.html')

def contact(request):
  return render(request,'contact.html')

def course(request):  
  course = models.Course.objects.all()
  courses = {'menu':course}
  return render(request,'course.html',courses)

def instructors(request):  
  instructor = models.Instructor.objects.all()
  instructors = {'menu':instructor}
  return render(request,'inst.html',instructors)

def topic(request,course_id):
  course  = models.Course.objects.get(pk=course_id)
  topics = models.Topic.objects.filter(course = course)
  return render(request,'topic.html',{'course':course,'topics':topics})

def Courseadmin(request,instructor_id):
  instructor = models.Instructor.objects.get(instructor_id = instructor_id)
  course = models.Course.objects.get(pk = instructor.course.id)
  topics = models.Topic.objects.filter(course = course)

  return render(request,'Courseadmin.html',{'course':course,'topics':topics, 'instructor':instructor})

"""
def student_view(request):
  if request.method == 'POST':
    student_id = request.POST.get('student_id')
    password = request.POST.get('password')
    print("id: ", student_id)
    try:
      student = models.Student.objects.get(student_id = student_id, password=password)
      cohort = models.Cohort.objects.get(pk = student.cohort.id)
      course = models.Course.objects.get(pk = student.course.id)
      topics = models.Topic.objects.filter(course = course)
      print("student: ", student)
      print("topics: ",topics)
      return render(request,'students.html',{'student':student,'topics':topics,'cohort':cohort})
    except models.Student.DoesNotExist:
      messages.error(request,'credentials not matching')
      return render(request,'student_login.html')
  else:
    return render(request,'student_login.html')

def instructor_view(request):
  cohorts = models.Cohort.objects.all()
  if request.method == 'POST':
    instructor_id = request.POST.get('instructor_id')
    password = request.POST.get('password')
    print("id: ", instructor_id)
    try:
      instructor = models.Instructor.objects.get(instructor_id = instructor_id, password=password)
      course = models.Course.objects.get(pk = instructor.course.id)
      topics = models.Topic.objects.filter(course = course)
      print("instructor: ", instructor)
      print("topics: ",topics)
      return render(request,'instructor.html',{'instructor':instructor,'topics':topics,'cohorts':cohorts})
    except models.Instructor.DoesNotExist:
      messages.error(request,'credentias not matching')
      return render(request,'instructor_login.html')
  else:
    return render(request,'instructor_login.html')

"""

def createnotes(request, instructor_id):
  if request.method == "POST":
    form = forms.TopicForm(request.POST, request.FILES)
    print('id',instructor_id)
    if form.is_valid():
      topic = form.save(commit=False)
      instructor = models.Instructor.objects.get(instructor_id = instructor_id)
      topic_course = models.Course.objects.get(pk = instructor.course.id)
      print('course: ', topic_course)
      topic_name = request.POST.get('name')
      topic_description = request.POST.get('description')
      topic_content = request.FILES.get('content')
      topic, created = models.Topic.objects.get_or_create(name = topic_name)
      topic.description = topic_description
      topic.content = topic_content
      topic.course = topic_course
      topic.save()
      return redirect(reverse('base:Courseadmin', kwargs={'instructor_id': instructor_id}))
  else :
    form = forms.TopicForm()

  return render(request,'create_notes.html',{'form':form})
  
def notes(request,topic_id):
  topic = models.Topic.objects.get(id = topic_id)
  return render(request, 'notes.html', {'topic':topic})

def updatenotes(request, instructor_id, topic_id):
  topic = models.Topic.objects.get(pk=topic_id)
  form = forms.TopicForm(instance=topic)
  if request.method == "POST":
    instructor = models.Instructor.objects.get(instructor_id = instructor_id)
    topic_course = models.Course.objects.get(pk = instructor.course.id)
    print('course: ', topic_course)
    topic_name = request.POST.get('name')
    topic_description = request.POST.get('description')
    topic_content = request.FILES.get('content')
    topic, created = models.Topic.objects.get_or_create(name = topic_name)
    topic.description = topic_description
    topic.content = topic_content
    topic.course = topic_course
    topic.save()

    return redirect(reverse('base:Courseadmin', kwargs={'instructor_id': instructor_id}))
  return render(request,'create_notes.html',{'form':form})

def changepassword(request, userid):
  user = models.Student.objects.filter(student_id = userid).exists()
  if request.method == "POST":
    if user:
      student = models.Student.objects.get(student_id = userid)
      if student.password == request.POST.get('oldpassword'):
        cohort = models.Cohort.objects.get(pk = student.cohort.id)
        course = models.Course.objects.get(pk = student.course.id)
        topics = models.Topic.objects.filter(course = course)
        if request.POST.get('newpassword') == request.POST.get('newcpnfpassword'):
          student.password = request.POST.get('newpassword')
          student.save()
          #return render(request,'students.html',{'student':student,'topics':topics,'cohort':cohort})
          return render(request,'login.html')
        else:
          messages.error(request,"passwords must be the same")
          return render(request,'change_password.html',{'userid':userid})
      else:
        messages.error(request,"invalid old password")
        return render(request,'change_password.html',{'userid':userid})
    else:
      instructor = models.Instructor.objects.get(instructor_id = userid)
      if instructor.password == request.POST.get('oldpassword'):
        cohorts = models.Cohort.objects.all()
        course = models.Course.objects.get(pk = instructor.course.id)
        topics = models.Topic.objects.filter(course = course)
        if request.POST.get('newpassword') == request.POST.get('newcpnfpassword'):
          instructor.password = request.POST.get('newpassword')
          instructor.save()
          #return render(request,'instructor.html',{'instructor':instructor,'topics':topics,'cohorts':cohorts})
          return render(request,'login.html')
        else:
          messages.error(request,"passwords must be the same")
          return render(request,'change_password.html',{'userid':userid})
      else:
        messages.error(request,"in valid old password")
        return render(request,'change_password.html',{'userid':userid})
  else:
    return render(request,'change_password.html',{'userid':userid})

def deletenotes(request, instructor_id, topic_id):
  topic = models.Topic.objects.get(pk = topic_id)

  if request.method == "POST":
    topic.delete()
    return redirect(reverse('base:Courseadmin', kwargs={'instructor_id': instructor_id}))
  return render(request,'delete.html',{'obj':topic})

def cohort(request,cohort_id,course_id, Id):
  cohort = models.Cohort.objects.get(id = cohort_id)
  cohort_messages = cohort.message_set.filter(course_id = course_id).order_by('created')
  course = models.Course.objects.get(id = course_id)
  try:
    user = models.Student.objects.get(student_id = Id)
    Id = user.student_id
  except models.Student.DoesNotExist:
    user = models.Instructor.objects.get(instructor_id = Id)
    Id = user.instructor_id
  if request.method == 'POST':
    if course.id == course_id:
      message = models.Message.objects.create(
        cohort = cohort,
        course = course,
        user = user,
        body = request.POST.get('body')
      )    
    return redirect(reverse('base:cohort', kwargs={'cohort_id':cohort_id,'course_id':course_id, 'Id':Id}))
  print("Id", Id)
  context = {'cohort':cohort,'cohort_messages':cohort_messages,'course':course, 'user':user, 'Id':Id}
  return render(request,'cohort.html',context)

def deletemessage(request, course_id,cohort_id, message_id, Id):
  message = models.Message.objects.get(pk = message_id)

  if request.method == "POST":
    message.delete()
    return redirect(reverse('base:cohort', kwargs={'cohort_id':cohort_id, 'course_id':course_id, 'Id':Id}))
  return render(request,'delete.html',{'obj':message})

def setexercise(request, instructor_id, topic_id):
  topic = models.Topic.objects.get(id = topic_id)
  if request.method == "POST":
    choice = models.Choice.objects.create(
      A = request.POST.get('A'),
      B = request.POST.get('B'),
      C = request.POST.get('C'),
      D = request.POST.get('D'),
    )
    exercise = models.Exercise.objects.create(
      Question = request.POST.get('Question'),
      choice = choice,
      Answer = request.POST.get('Answer'),
      topic = topic,
    )
    return redirect(reverse('base:Courseadmin', kwargs={'instructor_id': instructor_id}))
  return render (request,'setting_exercise.html')

def deleteexercise(request, id, topic_id, exercise_id):
  exercise = models.Exercise.objects.get(id = exercise_id)
  if request.method == "POST":
    exercise.delete()
    return redirect(reverse('base:exercise', kwargs={'user_id': id, 'topic_id': topic_id}))
  return render(request,'delete.html',{'obj':exercise})

def exercise(request, user_id, topic_id):
  topic = get_object_or_404(models.Topic, id=topic_id)
  exercises = models.Exercise.objects.filter(topic=topic)
  user = None
  student = False
  submittedexercises={}

  if request.method == "POST":
    answer = request.POST.get('Answer')
    Id = request.POST.get('exerciseid')
    print('ans: ',answer)
    print('id: ',Id)
    sms = mark(user_id,Id,answer)
    print("sms: ",sms)

  try:
    user = models.Student.objects.get(student_id=user_id)
    student = True
    
    for exercise in exercises:
      submissions = models.StudentExerciseSubmission.objects.filter(student=user,exercise=exercise)
      for submission in submissions:
        submittedexercises[exercise.id] = submission.message


    print("studentname: ", user.name)
    print("subexe: ",submittedexercises)
  except models.Student.DoesNotExist:
    try:
      user = models.Instructor.objects.get(instructor_id=user_id)
      print("instructor: ",user.name)
    except models.Instructor.DoesNotExist:
      pass
  print('student: ',student)
  context = {'user':user, 'exercises':exercises, 'topic':topic, 'student':student, 'submittedexercises':submittedexercises}
  return render(request,'exercise.html', context)

def mark(student_id, exercise_id, answer):
  student = models.Student.objects.get(student_id = student_id)
  exercise = models.Exercise.objects.get(id = exercise_id)
  #print("exerecise: ",exercise)
  submission_exists = models.StudentExerciseSubmission.objects.filter(student=student, exercise=exercise).exists()
  
  if not submission_exists:
    if answer == exercise.Answer:
      student.score += 5
      student.save()
      message = "Correct"
      
    else:
      message = "Wrong"

    submission = models.StudentExerciseSubmission.objects.create(student=student, exercise=exercise, submitted=True, message=message)  
    print("message: ", submission.message)
    return submission.message
          
  else:
    submission = models.StudentExerciseSubmission.objects.get(student=student, exercise=exercise)
    print("message: ", submission.message)
    #print("subexerecise: ",submission.exercise.id)
    return submission.message
    
def send_reset_email_to_user(request, userid):
  user = None
  if models.Student.objects.filter(student_id = userid).exists():
    user = models.Student.objects.get(student_id = userid)
  else:
    user = models.Instructor.objects.get(instructor_id=userid)
  
  resetcode = get_random_string(length=6, allowed_chars='0123456789')
  subject = 'Password Reset Pin'
  message = render_to_string('reset_email.txt', {
    'user': user,
    'resetcode': resetcode
  })
  from_email = settings.COMPANY_EMAIL
  recipient_list = [user.email]
  
  send_mail(subject, message, from_email, recipient_list)

  user.reset_pin = resetcode
  user.save()
  messages.success(request,"Email sent successfully!")  
  return render(request, 'emailsent.html',{'userid':userid})

def send_email(request, userid):
  user = None
  if models.Student.objects.filter(student_id = userid).exists():
    user = models.Student.objects.get(student_id = userid)
  else:
    user = models.Instructor.objects.get(instructor_id=userid)

  return render(request, 'forgotpassword.html', {'userid':userid, 'user':user})

def resetpassword(request, userid):
  user = models.Student.objects.filter(student_id = userid).exists()
  if request.method == "POST":
    if user:
      student = models.Student.objects.get(student_id = userid)
      if student.reset_pin == request.POST.get('resetcode'):
        cohort = models.Cohort.objects.get(pk = student.cohort.id)
        course = models.Course.objects.get(pk = student.course.id)
        topics = models.Topic.objects.filter(course = course)
        if request.POST.get('newpassword') == request.POST.get('newcpnfpassword'):
          student.password = request.POST.get('newpassword')
          student.reset_pin = ""
          student.save()
          return render(request,'students.html',{'student':student,'topics':topics,'cohort':cohort})
        else:
          messages.error(request,"passwords must be the same")
          return render(request,'reset_password.html',{'userid':userid})
      else:
        messages.error(request,"reset pin might be invalid or expired.")
        return render(request,'reset_password.html',{'userid':userid})
    else:
      instructor = models.Instructor.objects.get(instructor_id = userid)
      if instructor.reset_pin == request.POST.get('resetcode'):
        cohorts = models.Cohort.objects.all()
        course = models.Course.objects.get(pk = instructor.course.id)
        topics = models.Topic.objects.filter(course = course)
        if request.POST.get('newpassword') == request.POST.get('newcpnfpassword'):
          instructor.password = request.POST.get('newpassword')
          instructor.reset_pin=""
          instructor.save()
          return render(request,'instructor.html',{'instructor':instructor,'topics':topics,'cohorts':cohorts})
        else:
          messages.error(request,'passwords must be the same')
          return render(request,'reset_password.html',{'userid':userid})
      else:
        messages.error(request,'reset pin might be invalid or expired.')
        return render(request,'reset_password.html',{'userid':userid})
  else:
    return render(request,'reset_password.html',{'userid':userid})

def login_view(request):
  form = LoginForm()
  if request.method == 'POST':
    print('username: ',request.POST.get('username'))
    print('password: ',request.POST.get('password'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      models.Student.objects.get(student_id = request.POST.get('username'), password=request.POST.get('password'))
      student = models.Student.objects.get(student_id = request.POST.get('username'), password=request.POST.get('password'))
      cohort = models.Cohort.objects.get(pk = student.cohort.id)
      course = models.Course.objects.get(pk = student.course.id)
      topics = models.Topic.objects.filter(course = course)
      print("student: ", student)
      print("topics: ",topics)
      return render(request,'students.html',{'student':student,'topics':topics,'cohort':cohort})
    
    except models.Student.DoesNotExist:
      try:
        models.Instructor.objects.get(instructor_id = request.POST.get('username'), password=request.POST.get('password'))
        cohorts = models.Cohort.objects.all()
        instructor = models.Instructor.objects.get(instructor_id = request.POST.get('username'), password=request.POST.get('password'))
        course = models.Course.objects.get(pk = instructor.course.id)
        topics = models.Topic.objects.filter(course = course)
        print("instructor: ", instructor)
        print("topics: ",topics)
        return render(request,'instructor.html',{'instructor':instructor,'topics':topics,'cohorts':cohorts})
    
      except models.Instructor.DoesNotExist:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('base:user_view', kwargs={'userid': user.id}))  # Redirect to a success page.
        else:
            # Invalid login credentials
            messages.error(request,'credentias not matching')
  else:
    form = LoginForm()
  return render(request, 'login.html', {'form': form})

def create_post(request):
  if request.method == 'POST':
      post_form = PostForm(request.POST)
      media_formset = MediaFormSet(request.POST, request.FILES)

      if post_form.is_valid() and media_formset.is_valid():
          post = post_form.save(commit=False)
          post.author = request.user
          post.save()

          media_formset.instance = post
          media_formset.save()

          return redirect('base:post')
  else:
      post_form = PostForm()
      media_formset = MediaFormSet()

  return render(request, 'create_post.html', {
      'post_form': post_form,
      'media_formset': media_formset
  })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    like, created = models.Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # Unlike the post if it was already liked
    return redirect('base:post')

def post_detail(request):
  posts = models.Post.objects.all().order_by('-created_at')
  print("posts: ",posts)
  return render(request, 'post_detail.html', {'posts': posts})

@login_required
def user_view(request, userid):
  posts = models.Post.objects.all().order_by('-created_at')
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  students = models.Student.objects.filter(
    Q(name__icontains=q)|
    Q(course__name__icontains=q)|
    Q(school__name__icontains=q)
  )
  #b = request.GET.get('b') if request.GET.get('b') != None else ''
  instructors = models.Instructor.objects.filter(
    Q(name__icontains=q)|
    Q(course__name__icontains=q)|
    Q(school__name__icontains=q)
  )
  return render(request,"user.html",{'students':students, 'instructors':instructors, 'posts': posts})

def deletepost(request, post_id, Id):
  post = models.Post.objects.get(pk = post_id)

  if request.method == "POST":
    post.delete()
    return redirect(reverse('base:user_view', kwargs={'userid':Id}))
  return render(request,'delete.html',{'obj':post})


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_400(request, exception):
    return render(request, '400.html', status=400)



