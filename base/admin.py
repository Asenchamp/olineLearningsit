from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student,Instructor,Course,Cohort,School
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('student_id', 'score', 'password')  # Make student_id and score read-only
    fields = ('name', 'student_image', 'email', 'course', 'cohort', 'school', 'student_id', 'score')  # Define the order of fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only generate student_id for new objects
            prefix = "DIY-S-"
            unique_id = get_random_string(length=6, allowed_chars='0123456789')
            obj.student_id = f"{prefix}{unique_id}"
        super().save_model(request, obj, form, change)

        if not change:  # Only send email for new objects
            self.send_welcome_email(obj)

    def send_welcome_email(self, student):
        subject = "Welcome to Our Platform"
        message = render_to_string('student_welcome_email.txt', {
            'student': student,
        })
        send_mail(subject, message, settings.COMPANY_EMAIL, [student.email])




class InstructorAdmin(admin.ModelAdmin):
    readonly_fields = ('instructor_id', 'password')  # Make student_id and score read-only
    fields = ('name', 'instructor_image', 'email', 'course', 'school', 'admin')  # Define the order of fields


    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only generate student_id for new objects
            prefix = "DIY-I-"
            unique_id = get_random_string(length=12, allowed_chars='0123456789')
            obj.student_id = f"{prefix}{unique_id}"
        super().save_model(request, obj, form, change)

        if not change:  # Only send email for new objects
            self.send_welcome_email(obj)

    def send_welcome_email(self, instructor):
        subject = "Welcome to Our Platform"
        message = render_to_string('instructor_welcome_email.txt', {
            'instructor': instructor,
        })
        send_mail(subject, message, settings.COMPANY_EMAIL, [instructor.email])


admin.site.register(Student, StudentAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(School)
admin.site.register(Cohort)
admin.site.register(Course)
admin.site.site_title = "DIY ADMIN"
admin.site.site_header = "DO IT YOURSELF"
admin.site.index_title = "DO IT YOURSELF"