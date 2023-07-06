from django.contrib import admin
from .models import Student, Course, Lecturer, CarryMark

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(CarryMark)
