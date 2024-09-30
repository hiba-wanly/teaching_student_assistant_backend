# Generated by Django 4.2.15 on 2024-09-29 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_student_user_alter_studentinfo_academic_year'),
        ('homework', '0003_alter_homework_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkLOG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.FloatField()),
                ('recived', models.BooleanField(default=False)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homework.homework')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.student')),
            ],
        ),
    ]