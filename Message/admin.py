from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CourseUnits, User_details, Myunits, Messages

class Details(admin.ModelAdmin):
	list_display = ('member','depart','course','studyear','sem')
	list_filter = ('member',)
	search_fields = ['member','depart']
class Subjects(admin.ModelAdmin):
	list_display = ('depart','courseunit')
	list_filter = ('courseunit',)
	search_fields = ['depart','courseunit']


class Cunit(admin.ModelAdmin):
	list_display = ('student','courseunit','studyear','sem')
	list_filter = ('student',)
	search_fields = ['student','courseunit']

class Notice(admin.ModelAdmin):
	list_filter = ('destiny',)
	list_display = ('destiny','text','sender','create','file')
	search_fields = ['destiny','text']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(CourseUnits, Subjects)
admin.site.register(User_details,Details)
admin.site.register(Myunits,Cunit)
admin.site.register(Messages,Notice)
