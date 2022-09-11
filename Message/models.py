from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
	contact = models.CharField(max_length=13, unique=True)
	username = models.CharField(max_length=100,default="none")
	reg_no = models.CharField(max_length=10,unique=True,blank=True,null=True)
	roles = models.CharField(max_length=10,blank=True,null=True)

	USERNAME_FIELD = 'contact'

	REQUIRED_FIELDS = ['username']
	def __str__(self):
		return  self.first_name

class User_details(models.Model):
	member = models.ForeignKey(User,on_delete=models.CASCADE)
	depart = models.CharField(max_length=100,blank=True,null=True)
	course = models.CharField(max_length=100,blank=True,null=True)
	studyear = models.CharField(max_length=1,blank=True,null=True)
	sem = models.CharField(max_length=1,blank=True,null=True)
	approved = models.CharField(max_length=3,default='No')

class CourseUnits(models.Model):
	depart = models.CharField(max_length=100,blank=True,null=True)
	courseunit = models.CharField(max_length=100)

class Myunits(models.Model):
	student = models.ForeignKey(User,on_delete=models.CASCADE)
	courseunit = models.CharField(max_length=100)
	studyear = models.CharField(max_length=1,blank=True,null=True)
	sem = models.CharField(max_length=1,blank=True,null=True)


class Messages(models.Model):
	sender  = models.ForeignKey(User,on_delete=models.CASCADE)
	destiny = models.CharField(max_length=100,blank=True,null=False)
	text = models.TextField()
	file = models.FileField(upload_to='files', null=True, blank=True)
	create = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-create']