# Generated by Django 5.0.6 on 2024-07-18 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_alter_topic_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='cohort',
        ),
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentexercisesubmission',
            name='student',
        ),
        migrations.RemoveField(
            model_name='studentexercisesubmission',
            name='exercise',
        ),
        migrations.DeleteModel(
            name='Instructor',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='StudentExerciseSubmission',
        ),
    ]