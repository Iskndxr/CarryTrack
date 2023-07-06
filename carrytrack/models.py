from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Student(models.Model):
    matricID = models.CharField(max_length=10, unique=True, primary_key=True)
    studentName = models.CharField(max_length=50)
    studentPhone = models.CharField(null=True,max_length=12)
    studentImage = models.ImageField(upload_to='media', null=True)
    currentSemester = models.CharField(default='1', max_length=1, validators=[MaxValueValidator(9)])
    password = models.CharField(max_length=50)
    mentorID = models.ForeignKey('Lecturer', on_delete=models.CASCADE, null=True)

class Course(models.Model):
    courseCode = models.CharField(max_length=10, unique=True, primary_key=True)
    courseName = models.CharField(max_length=50)
    courseCredit = models.IntegerField(default=0, validators=[MaxValueValidator(4)])
    maxCarryMark = models.IntegerField(null=True, validators=[MaxValueValidator(70)])

class Lecturer(models.Model):
    lecturerID = models.CharField(max_length=10, unique=True, primary_key=True)
    lecturerName = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class CarryMark(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    assesment1 = models.IntegerField(default=0,null=True,validators=[MaxValueValidator(30)])
    assesment2 = models.IntegerField(default=0,null=True,validators=[MaxValueValidator(30)])
    assesment3 = models.IntegerField(default=0,null=True,validators=[MaxValueValidator(30)])
    assesment4 = models.IntegerField(default=0,null=True,validators=[MaxValueValidator(30)])
    is_reviewed = models.BooleanField(null=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'course']