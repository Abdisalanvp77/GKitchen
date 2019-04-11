from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import uuid, random
# Create your models here.



class RegisteredUser(models.Model):
    userName = models.CharField(max_length=200)
    emailField = models.EmailField()
    passwordField = models.CharField(max_length=18)
    passwordConfirmField = models.CharField(max_length = 18)

    def __str__(self):
        return self.userName
class Booking(models.Model):
    def number():
        no = Booking.objects.count()
        return no + 1

    id = models.AutoField(primary_key=True, default=number,
                          editable=False, unique=True)
    eventName = models.CharField(max_length=200)
    bookerName = models.CharField(max_length=200)
    bookerEmailField = models.EmailField()
    phoneField = models.CharField(max_length=200)
    eventStartTime = models.DateField(default=datetime.now, blank=False)
    eventEndTime = models.DateField(default=datetime.now, blank=False)
    numberOfPeople = models.IntegerField(default=0)
    comment = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.eventName
    
    
    # id = generate_id()
class Contacted(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    contactEmail = models.EmailField()
    subjectAreaText = models.TextField()

    def __str__(self):
        return self.firstName
