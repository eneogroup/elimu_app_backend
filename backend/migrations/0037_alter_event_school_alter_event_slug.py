# Generated by Django 5.1.1 on 2024-10-10 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0036_remove_parentofstudent_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.school'),
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
