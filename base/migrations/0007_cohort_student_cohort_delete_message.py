# Generated by Django 5.0.1 on 2024-05-07 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_instructor_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='cohort',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.cohort'),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]