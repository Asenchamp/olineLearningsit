# Generated by Django 5.0.1 on 2024-05-02 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_topic_instructor_instructor_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.course'),
        ),
    ]
