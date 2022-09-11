from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import User
from django.contrib.auth import login, authenticate,get_user_model, logout

# Create your views here.
class Login_view(View):
	def get(self, request):
		if request.user.is_authenticated:
			if(request.user.is_staff):
				return redirect("/admins/")
			elif(request.user.roles == "Lecturer"):
				return redirect("/home/")
			else:
				return redirect("/student/")
		return render(request,"page-login.html",{})
	def post(self, request):
		contact = request.POST.get('contact')
		password = request.POST.get('password')
		user = authenticate(contact=contact,password=password)
		try:
			login(request,user)
			# if(request.user.is_staff):
			# 	return redirect("/admins/")
			# elif(request.user.roles == "Lecturer"):
			# 	return redirect("/home/")
			# else:
			# 	return redirect("/student/")
			return HttpResponse(1)
		except:
			return HttpResponse("failed to login")