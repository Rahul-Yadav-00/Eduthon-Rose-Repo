# Generated by Django 3.1.1 on 2020-09-05 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classname', models.CharField(max_length=50)),
                ('classsubject', models.CharField(max_length=30)),
                ('classCode', models.SlugField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('classdecription', models.TextField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_of_class', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassStudents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='which_classroom_join', to='classroom.classroom')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_who_join', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'classroom')},
            },
        ),
    ]
