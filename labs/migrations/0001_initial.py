# Generated by Django 4.2.15 on 2024-09-03 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Labs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_full_mark', models.FloatField()),
                ('number_of_labs', models.IntegerField()),
                ('percentage', models.FloatField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subject.subject')),
            ],
        ),
    ]
