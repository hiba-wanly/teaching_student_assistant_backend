# Generated by Django 4.2.15 on 2024-09-30 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0004_alter_subject_academic_year_alter_subject_semester'),
        ('labs', '0003_labslog'),
    ]

    operations = [
        migrations.AddField(
            model_name='labslog',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='subject.subject'),
        ),
    ]
