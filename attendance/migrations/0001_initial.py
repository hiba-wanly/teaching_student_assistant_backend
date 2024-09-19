# Generated by Django 4.2.15 on 2024-09-18 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('day', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('percentage', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceLOG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('attendance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='attendance.attendance')),
            ],
        ),
    ]
