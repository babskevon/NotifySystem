from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import User, User_details, CourseUnits, Myunits, Messages
from django.contrib.auth import login, authenticate,get_user_model, logout
from datetime import *
from .Sendmessage import Sendmessage

# Create your views here.
class Register_view(View):
	def get(self, request):
		data = {}
		return render(request, "page-register.html", data)

	def post(self, request):
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		contact = request.POST.get('telephone')
		role = request.POST.get('role')
		password = request.POST.get('password')
		try:
			user = User.objects.create_user(contact=contact,password=password,first_name=fname,last_name=lname,roles=role,username=role)
			user.save()
			User_details.objects.create(member=user)
			# user = authenticate(username=username, password=password)
			login(request,user)
			return HttpResponse(1)
		except:
			return HttpResponse('Server error, please try again')
		# return HttpResponse(contact)


class Student_view(View):
	def get(self, request):
		# redirect lecturer to message page
		if(request.user.roles == 'Lecturer'):
			return redirect("/home/")

		# end redirect to send message

		try:
			subjects = CourseUnits.objects.all()
			details = User_details.objects.get(member=request.user)
			myunits = Myunits.objects.filter(student=request.user,studyear=details.studyear,sem=details.sem)
			notes = Messages.objects.filter(destiny__in=[x.courseunit for x in myunits]).exclude(file__isnull=True).exclude(file__exact='')
			print([x.courseunit for x in myunits])	
			print([x.destiny for x in notes])	
		except:
			myunits = []
			notes = []
		data = {
			'subjects':subjects,
			'details':details,
			'myunits':myunits,
			'notes':notes
		}
		return render(request,"student-register.html",data)

	def post(self, request):
		course = request.POST.get('course')
		year = request.POST.get('year')
		units = request.POST.get('units')
		sem = request.POST.get('sem')
		reg = request.POST.get('reg')
		# print(units," kevin's units")

		# list of all course units
		course_units = units.split(" ")

		# get user object
		user = User.objects.get(contact=request.user.contact)
		try:
			user.reg_no = reg
			user.save()
			try:
				detail = User_details.objects.get(member=user)
			except:
				detail = User_details.objects.create(member=user,depart=course,course=course,studyear=year,sem=sem)

			detail.depart = course
			detail.studyear = year
			detail.sem = sem
			detail.course = course
			detail.save()
			try:
				Myunits.objects.filter(student=user).delete()
				for unit in course_units:
					Myunits.objects.create(student=user,studyear=year,sem=sem,courseunit=unit)
			except:
				pass
			return HttpResponse(1)
		except:
			pass

		
class Home_view(View):
	def post(self, request):
		msg = request.POST.get('msg')
		subject = request.POST.get('subject')
		files = request.POST.get('files')
		if(files == 'Yes'):
			file = request.FILES['file']
			print(files)
		else:
			print(files)
		# subject = subject.split(" ")
		sender = "\nFrom: " + request.user.first_name + " " + request.user.last_name
		# sender = subject + "\n" + sender + msg
		msged = msg + sender + " " + subject
		try:
			contact = Myunits.objects.filter(courseunit=subject)
			contacts = ["+256" + x.student.contact[-9:] for x in contact]
			print(contacts)
			if(User_details.objects.get(member=request.user).approved == 'Yes'):
				response = Sendmessage(msged,contacts)
				# print()
				# print(response['SMSMessageData']['Recipients'])
				if(files == 'Yes'):
					try:
						Messages.objects.create(sender=request.user,text=msg,destiny=subject,file=file)
					except:
						pass
				else:
					try:
						Messages.objects.create(sender=request.user,text=msg,destiny=subject)
					except:
						pass
				verify = 0
				count = 0
				for state in response['SMSMessageData']['Recipients']:
					if(state['status'].upper().strip() == "success".upper().strip()):
						verify = verify + 1
						count = count + 1
					else:
						count = count + 1

				return HttpResponse("{}/{} messages have been successfully sent".format(verify,count))
		except:
			return HttpResponse("Message failed to send, please try again")


	def get(self, request):
		if(request.user.is_authenticated):
			if(request.user.roles != "Lecturer"):
				if(request.user.is_staff != True):
					return redirect("/")
			# elif(request.user.is_staff):
			# 	pass
		else:
			return redirect("/")
		subjects = CourseUnits.objects.all()
		data = {
			'subjects':subjects,
			'details':User_details.objects.get(member=request.user),
		}
		return render(request,"home.html",data)




class Lecturer_view(View):
	def get(self, request):
		if(request.user.is_authenticated != True):
			return redirect('/')
		try:
			messages = Messages.objects.filter(sender=request.user)
		except:
			messages = None
		data = {
			'details':User_details.objects.get(member=request.user),
			'messages':messages
		}
		return render(request,"lecturer.html", data)
	def post(self, request):
		depart = request.POST.get('depart')
		
		try:
			update = User_details.objects.get(member=request.user)
			update.depart = depart
			update.approved = "No"
			update.save()
			return HttpResponse(1)
		except:
			User_details.objects.create(member=request.user,depart=depart)
			return HttpResponse(1)


class Signout(View):
	def get(self, request):
		logout(request)
		return redirect('/')