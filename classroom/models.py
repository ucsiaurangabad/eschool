from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)

    def __str__(self):
        return self.name

class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    school_id = models.ForeignKey(School,on_delete=models.CASCADE,blank=False,null=False)
    email = models.CharField(max_length=50)

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    school_id = models.ForeignKey(School,on_delete=models.CASCADE,blank=False,null=False)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    school_id = models.ForeignKey(School,on_delete=models.CASCADE,blank=False,null=False)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=12)
    standard = models.IntegerField(default=5)


