from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Course, Lecturer, CarryMark
from .forms import RegistrationForm
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages

def homeStudent(request):
    student_matricID = request.session.get('student_matricID')

    if student_matricID:
        try:
            student = Student.objects.get(matricID=student_matricID)
            carrymarks = CarryMark.objects.filter(student=student)
            carrymark_count = carrymarks.count()

            context = {
                'carrymarks': carrymarks,
                'carrymark_count': carrymark_count,
                'student': student,
            }

            return render(request, 'homeStudent.html', context)
        except Student.DoesNotExist:
            return redirect('login')
    else:
        return redirect('login')

def homeLecturer(request):
    lecturerID = request.session.get('lecturerID')
    students = Student.objects.filter(mentorID=lecturerID)
    context = {
        'students': students
    }
    return render(request, 'homeLecturer.html', context)

def login(request):
    if request.method == 'POST':
        matricID = request.POST.get('matricID')
        password = request.POST.get('password')

        if matricID and password:
            try:
                student = Student.objects.get(matricID=matricID)
            except Student.DoesNotExist:
                return render(request, 'login.html', {'login_error': 'Invalid login credentials. Please try again.'})

            if check_password(password, student.password):
                request.session['student_matricID'] = student.matricID
                return redirect('homeStudent')
            else:
                return render(request, 'login.html', {'login_error': 'Invalid login credentials. Please try again.'})
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def loginLecturer(request):
    if request.method == 'POST':
        lecturerID = request.POST.get('lecturerID')
        password = request.POST.get('password')

        lecturer = None

        if lecturerID and password:
            try:
                lecturer = Lecturer.objects.get(lecturerID=lecturerID)
            except Lecturer.DoesNotExist:
                return render(request, 'loginLecturer.html', {'login_error': 'Invalid login credentials. Please try again.'})

        if lecturer and lecturer.password == password:
            request.session['lecturerID'] = lecturer.lecturerID
            return redirect('homeLecturer')

        return render(request, 'loginLecturer.html', {'login_error': 'Invalid login credentials. Please try again.'})

    return render(request, 'loginLecturer.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        default_image = '/media/blank-person.jpg'

        if form.is_valid():
            matricID = form.cleaned_data['matricID']
            studentName = form.cleaned_data['studentName']
            password = form.cleaned_data['password']
            mentorID = form.cleaned_data['mentorID']

            hashed_password = make_password(password)

            try:
                mentor = Lecturer.objects.get(lecturerID=mentorID)
            except Lecturer.DoesNotExist:
                return redirect('register')

            try:
                student = Student.objects.get(matricID=matricID)
                return redirect('register')
            except Student.DoesNotExist:
                student = Student(matricID=matricID, studentName=studentName, password=hashed_password, mentorID=mentor ,studentImage=default_image)
                student.save()

                return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)

def add_course(request):
    context = {}

    if request.method == 'POST':
        student_matricID = request.session.get('student_matricID')

        if student_matricID:
            try:
                student = Student.objects.get(matricID=student_matricID)

                carrymark_count = CarryMark.objects.filter(student=student).count()

                if carrymark_count < 5:
                    selected_courses = request.POST.getlist('courses[]')
                    context['selected_courses'] = selected_courses
                    available_courses = Course.objects.exclude(carrymark__student=student)
                    context['available_courses'] = available_courses

                    duplicate_courses = []
                    for course_id in selected_courses:
                        if CarryMark.objects.filter(student=student, course_id=course_id).exists():
                            duplicate_courses.append(course_id)

                    if duplicate_courses:
                        context['duplicate_courses'] = duplicate_courses
                        return render(request, 'add_course.html', context) 

                    remaining_slots = 5 - carrymark_count

                    for i in range(min(remaining_slots, len(selected_courses))):
                        course_id = selected_courses[i]
                        course = Course.objects.get(pk=course_id)

                        if not CarryMark.objects.filter(student=student, course=course).exists():
                            CarryMark.objects.create(student=student, course=course)

                    return redirect('homeStudent')
            except Student.DoesNotExist:
                return redirect('login')

    student_matricID = request.session.get('student_matricID')
    if student_matricID:
        try:
            student = Student.objects.get(matricID=student_matricID)
            carrymark_count = CarryMark.objects.filter(student=student).count()
            context['carrymark_count'] = carrymark_count
        except Student.DoesNotExist:
            return redirect('login')

    available_courses = Course.objects.exclude(carrymark__student=student)
    context['available_courses'] = available_courses
    return render(request, 'add_course.html', context)
    
def update_carrymark(request,pk):
    try:
        carrymark = CarryMark.objects.get(pk=pk)
    except CarryMark.DoesNotExist:
        return redirect('homeStudent')

    if request.method == 'POST':
        assesment1 = int(request.POST.get('assessment1'))
        assesment2 = int(request.POST.get('assessment2'))
        assesment3 = int(request.POST.get('assessment3'))
        assesment4 = int(request.POST.get('assessment4'))

        carrymark.assesment1 = assesment1
        carrymark.assesment2 = assesment2
        carrymark.assesment3 = assesment3
        carrymark.assesment4 = assesment4
        
        carrymark.is_reviewed = None
        carrymark.save()

        return redirect('homeStudent')

    context = {'carrymark': carrymark}
    return render(request, 'update_carrymark.html', context)

def delete_carrymark(request,pk):
    carrymark = get_object_or_404(CarryMark, pk=pk)

    if request.method == 'POST' and 'confirm-delete' in request.POST and request.POST['confirm-delete'] == 'yes':
        carrymark.delete()
        return redirect('homeStudent')

    context = {'carrymark': carrymark}
    return render(request, 'delete_carrymark.html', context)

def save_courses(request):
    if request.method == 'POST':
        selected_courses = request.POST.getlist('courses[]') 
        
        if len(selected_courses) < 1 or len(selected_courses) > 5:
            return redirect('add_course')
        
        student_matricID = request.session.get('student_matricID')
        if student_matricID:
            try:
                student = Student.objects.get(matricID=student_matricID)
                
                carrymark_count = CarryMark.objects.filter(student=student).count()
                remaining_slots = 5 - carrymark_count
                
                if len(selected_courses) > remaining_slots:
                    return redirect('add_course')
                
                for course_id in selected_courses:
                    course = Course.objects.get(pk=course_id)
                    carry_mark = CarryMark(student=student, course=course)
                    carry_mark.save()
                
                return redirect('homeStudent')
            
            except Student.DoesNotExist:
                return redirect('login')
            
            except Course.DoesNotExist:
                return redirect('add_course')
            
        else:
            return redirect('login')
    
    else:
        return redirect('add_course')

def studentCarrymark(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)
    context = {
        'student': student
    }
    return render(request, 'studentCarrymark.html', context)

def review_carrymark(request, pk):
    if request.method == 'POST':
        carrymark = get_object_or_404(CarryMark, pk=pk)
        carrymark.is_reviewed = True
        carrymark.save()
        return HttpResponse(status=200) 
    else:
        return HttpResponseBadRequest("Invalid request method")
    
def leaveRemarks(request, pk):
    carrymark = get_object_or_404(CarryMark, pk=pk)
    
    if request.method == 'POST':
        remarks = request.POST.get('remarks')
        carrymark.remarks = remarks 
        carrymark.save()

        return redirect ('studentCarrymark', carrymark.student.matricID)
    
    context = {
        'carryMark': carrymark
    }
    return render(request, 'leaveRemarks.html', context)

def studentImage(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)
    context = {
        'student': student
    }
    return render(request, 'homeStudent.html', context)

def studentProfile(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)
    context = {
        'student': student
    }
    return render(request, 'studentProfile.html', context)

def deleteProfile(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)
    if request.method == 'POST' and 'confirm-delete' in request.POST and request.POST['confirm-delete'] == 'yes':
        student.delete()
        return redirect('login')

    context = {'student': student}
    return render(request, 'delete_profile.html', context)


def updateProfile(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)

    if request.method == 'POST':
        mentorID = request.POST['mentorID']

        try:
            lecturer = Lecturer.objects.get(lecturerID=mentorID)
        except Lecturer.DoesNotExist:
            return render(request, 'studentProfile.html', {'student': student , 'update_error': 'Invalid Mentor ID'})

        student.mentorID = lecturer
        student.studentPhone = request.POST['studentPhone']
        student.currentSemester = request.POST['currentSemester']

        if 'studentImage' in request.FILES:
            student.studentImage = request.FILES['studentImage']

        student.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('homeStudent')

    context = {
        'student': student,
    }
    return render(request, 'studentProfile.html', context)

def removeStudent(request, matricID):
    student = get_object_or_404(Student, matricID=matricID)
    if request.method == 'POST' and 'confirm-delete' in request.POST and request.POST['confirm-delete'] == 'yes':
        student.mentorID = None
        student.save()
        return redirect('homeLecturer')

    context = {'student': student}
    return render(request, 'remove_student.html', context)

def logoutLecturer(request):
    request.session.clear()
    return redirect('loginLecturer')

def logoutStudent(request):
    request.session.clear()
    return redirect('loginStudent')