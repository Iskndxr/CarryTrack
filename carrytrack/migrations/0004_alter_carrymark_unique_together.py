# Generated by Django 4.2 on 2023-06-28 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrytrack', '0003_alter_carrymark_is_reviewed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carrymark',
            unique_together={('student', 'course')},
        ),
    ]