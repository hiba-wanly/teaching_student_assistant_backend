# Generated by Django 4.2.15 on 2024-09-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0003_subject_practical_mark_subject_total_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='academic_year',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='subject',
            name='semester',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
