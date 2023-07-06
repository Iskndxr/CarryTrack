from django import forms

class RegistrationForm(forms.Form):
    matricID = forms.CharField(max_length=100)
    studentName = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    mentorID = forms.CharField(max_length=100)