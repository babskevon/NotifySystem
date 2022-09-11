from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import User_details, User

# Create your views here.
class Admin_view(View):
	def get(self, request):
		if(request.user.is_authenticated):
			if(request.user.is_staff != True):
				return redirect("/")
		details = User_details.objects.get(member=request.user)
		year1 = User_details.objects.filter(course=details.depart,studyear=1).count()
		year2 = User_details.objects.filter(course=details.depart,studyear=2).count()
		year3 = User_details.objects.filter(course=details.depart,studyear=3).count()
		year4 = User_details.objects.filter(course=details.depart,studyear=4).count()
		lecturers  = User_details.objects.filter(member__roles="Lecturer",depart=details.depart)
		students = User_details.objects.filter(member__roles='Student',depart=details.depart)
		lect  = lecturers.count()
		data = {
			'year1':year1,
			'year2':year2,
			'year3':year3,
			'year4':year4,
			'lect':lect,
			'lects':lecturers,
			'details':details,
			'students':students
		}
		return render(request,"admin.html",data)

	def post(self, request):
		try:
			contact = request.POST.get('contact')
			user = User_details.objects.get(member__contact=contact)
			user.approved = 'Yes'
			user.save()
			return HttpResponse(1)
		except:
			pass

		try:
			del_user = request.POST.get('contactd')
			person = User.objects.get(contact=del_user)
			person.delete()
			return HttpResponse(1)
		except:
			pass

		try:
			decide = request.POST.get('decide')
			user = User_details.objects.get(member__contact=decide)
			user.approved = 'No'
			user.save()
			return HttpResponse(1)
		except:
			pass

		try:
			std = request.POST.get('std')
			person = User.objects.get(contact=std)
			print('\n\t','*****',person.first_name,'*****')
			person.delete()
			return HttpResponse(1)
		except:
			pass

		try:
			perm = request.POST.get('perm')
			person = User.objects.get(contact=perm)
			person.is_staff = True
			person.save()
			return HttpResponse(1)
		except:
			return HttpResponse("server error, please try again later")
		