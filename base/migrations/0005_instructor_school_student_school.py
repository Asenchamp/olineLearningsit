# Generated by Django 5.0.1 on 2024-05-02 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_student_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='school',
            field=models.CharField(default=False, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.CharField(default=False, max_length=100),
        ),
    ]