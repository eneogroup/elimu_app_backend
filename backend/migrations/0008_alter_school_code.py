# Generated by Django 5.1.1 on 2024-09-20 13:37

import backend.models.school_manager.school_manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_school_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='code',
            field=backend.models.school_manager.school_manager.UUID4Field(auto_created=True, blank=True, max_length=17, unique=True),
        ),
    ]
