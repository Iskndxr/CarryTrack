from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('homeStudent/', views.homeStudent, name='homeStudent'),
    path('homeLecturer/', views.homeLecturer, name='homeLecturer'),
    path('loginLecturer/', views.loginLecturer, name='loginLecturer'),
    path('register/', views.register, name='register'),
    path('add_course/', views.add_course, name='add_course'),
    path('update_carrymark/<int:pk>/', views.update_carrymark, name='update_carrymark'),
    path('delete_carrymark/<int:pk>/', views.delete_carrymark, name='delete_carrymark'),
    path('save_courses/', views.save_courses, name='save_courses'),
    path('studentCarrymark/<str:matricID>/', views.studentCarrymark, name='studentCarrymark'),
    path('review-carrymark/<int:pk>/', views.review_carrymark, name='review_carrymark'),
    path('leaveRemarks/<int:pk>/', views.leaveRemarks, name='leaveRemarks'),
    path('studentImage/', views.studentImage, name='studentImage'),
    path('studentProfile/<str:matricID>/', views.studentProfile, name='studentProfile'),
    path('deleteProfile/<str:matricID>/', views.deleteProfile, name='deleteProfile'),
    path('updateProfile/<str:matricID>/', views.updateProfile, name='updateProfile'),
    path('removeStudent/<str:matricID>/', views.removeStudent, name='removeStudent'),
    path('logoutLecturer/', views.logoutLecturer, name='logoutLecturer'),
]
