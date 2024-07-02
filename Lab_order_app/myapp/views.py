from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, TestPackageForm, LabResultForm, DoctorNoteForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import TestPackage
from django.contrib.auth.decorators import login_required
from django import forms

def base(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.user_type == 'P':
                    return redirect('patient')
                elif user.user_type == 'L':
                    return redirect('lab')
                elif user.user_type == 'D':
                    return redirect('doctor')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('base')


@login_required
def patient(request):
    if request.method == 'POST':
        form = TestPackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.username = request.user.username
            package.save()
            return redirect('patient')
    else:
        form = TestPackageForm()

    ordered_packages = TestPackage.objects.filter(user=request.user)
    completed_packages = TestPackage.objects.filter(user=request.user).exclude(glucose=None)

    return render(request, 'patient.html', {'form': form, 'ordered_packages': ordered_packages, 'completed_packages': completed_packages})

@login_required
def lab(request):
    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        package = TestPackage.objects.get(pk=package_id)
        form = LabResultForm(request.POST, instance=package)

        package.lab_username = request.user.username

        if package.package == 'basic':
            if 'tsh' in form.fields:
                form.fields['tsh'].widget = forms.HiddenInput()
            if 'ft3' in form.fields:
                form.fields['ft3'].widget = forms.HiddenInput()
            if 'ft4' in form.fields:
                form.fields['ft4'].widget = forms.HiddenInput()
        elif package.package == 'full':
            if 'tsh' in form.fields:
                form.fields['tsh'].widget = forms.TextInput()
            if 'ft3' in form.fields:
                form.fields['ft3'].widget = forms.TextInput()
            if 'ft4' in form.fields:
                form.fields['ft4'].widget = forms.TextInput()

        if form.is_valid():
            instance = form.save(commit=False)
            instance.date_result = timezone.now()  # Dodanie daty wyników badania
            instance.save()
            return redirect('lab')
    else:
        form = LabResultForm()

    ordered_packages = TestPackage.objects.filter(lab_username='default_lab', glucose__isnull=True)

    return render(request, 'lab.html', {'ordered_packages': ordered_packages, 'form': form})

@login_required
def doctor(request):
    if request.method == 'POST':
        form = DoctorNoteForm(request.POST)
        if form.is_valid():
            package_id = request.POST.get('package_id')
            package = TestPackage.objects.get(pk=package_id)
            package.doctor_notes = form.cleaned_data['doctor_notes']
            package.doctor_username = request.user.username
            package.date_diagnose = timezone.now()  # Dodanie daty diagnozy
            package.save()
            return redirect('doctor')
    else:
        form = DoctorNoteForm()

    pending_packages = TestPackage.objects.filter(doctor_username='default_doctor')

    return render(request, 'doctor.html', {'pending_packages': pending_packages, 'form': form})