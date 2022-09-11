from django.urls import path
# from Message.views import Home_view, Register_view, Student_view, Lecturer_view, Signout
from Message.login import Login_view
from Message.notify_admin import Admin_view
from Message.views import Register_view, Lecturer_view, Signout, Home_view, Student_view

urlpatterns = [
	path('', Login_view.as_view(), name='login'),
	path('sendmsg/',Home_view.as_view(), name='send'),
	path('signout/', Signout.as_view(), name='signout'),
	path('signup/', Register_view.as_view(), name='signup'),
	path('student/', Student_view.as_view(), name='student'),
	path('home/', Lecturer_view.as_view(), name='home'),
	path('admins/', Admin_view.as_view(), name='admins')
]