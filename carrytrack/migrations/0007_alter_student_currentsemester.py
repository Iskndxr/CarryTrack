# Generated by Django 4.2 on 2023-06-29 05:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrytrack', '0006_student_studentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='currentSemester',
            field=models.CharField(default='1', max_length=1, validators=[django.core.validators.MaxValueValidator(9)]),
        ),
    ]
