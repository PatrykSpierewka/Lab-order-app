from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    USER_CHOICES = (
        ('P', 'Pacjent'),
        ('L', 'Laboratorium'),
        ('D', 'Lekarz'),
    )
    user_type = models.CharField(max_length=1, choices=USER_CHOICES)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )


class TestPackage(models.Model):
    PACKAGE_CHOICES = [
        ('basic', 'Podstawowy pakiet zdrowia'),
        ('full', 'Pełny pakiet zdrowia'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, default='default_username')
    lab_username = models.CharField(max_length=150, default='default_lab')
    doctor_username = models.CharField(max_length=150, default='default_doctor')
    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    date_ordered = models.DateTimeField(auto_now_add=True)

    glucose = models.FloatField(null=True, blank=True)
    red_blood_cells = models.FloatField(null=True, blank=True)
    white_blood_cells = models.FloatField(null=True, blank=True)
    tsh = models.FloatField(null=True, blank=True)
    ft3 = models.FloatField(null=True, blank=True)
    ft4 = models.FloatField(null=True, blank=True)
    date_result = models.DateTimeField(auto_now_add=True)

    doctor_notes = models.TextField(blank=True)
    date_diagnose = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.get_package_display()}"