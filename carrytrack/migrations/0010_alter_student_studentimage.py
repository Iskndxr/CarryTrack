# Generated by Django 4.2 on 2023-06-29 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrytrack', '0009_alter_student_studentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='studentImage',
            field=models.ImageField(default='static/blank-person.jpg', upload_to='media'),
        ),
    ]
