from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import TestPackage
class SignUpForm(UserCreationForm):
    USER_CHOICES = (
        ('P', 'Pacjent'),
        ('L', 'Laboratorium'),
        ('D', 'Lekarz'),
    )
    user_type = forms.ChoiceField(choices=USER_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'user_type', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TestPackageForm(forms.ModelForm):
    class Meta:
        model = TestPackage
        fields = ['package']
        labels = {
            'package': 'Wybierz pakiet badań',
        }
        widgets = {
            'package': forms.RadioSelect
        }

class LabResultForm(forms.ModelForm):
    class Meta:
        model = TestPackage
        fields = ['glucose', 'red_blood_cells', 'white_blood_cells', 'tsh', 'ft3', 'ft4']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.package == 'basic':
            self.fields.pop('tsh')
            self.fields.pop('ft3')
            self.fields.pop('ft4')

class DoctorNoteForm(forms.ModelForm):
    doctor_notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))

    class Meta:
        model = TestPackage
        fields = ['doctor_notes']