from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			us = RrskCustomers.objects.get(user = request.user)
			return redirect('/dashboard/' + str(us.id))
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

