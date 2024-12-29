# Generated by Django 5.1.4 on 2024-12-27 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_presentation_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='presentation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classrooms', to='mainapp.presentation', verbose_name='Sunum'),
        ),
    ]