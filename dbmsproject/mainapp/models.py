from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    username = models.EmailField()
    password=models.CharField(max_length=50)
    registrationDate = models.DateField("Registration Date", auto_now_add=True)
    def __str__(self):
        return self.name
    

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    id = models.CharField(max_length=10, primary_key=True)
    phone_no = models.CharField(max_length=15)
    speciality = models.CharField(max_length=255)
    year_of_experience = models.IntegerField()

    def __str__(self):
        return self.name
    


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    