from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    # wrapper_func là 1 hàm sẽ thực thi những misc operations (checking,...) trước khi hàm chính - view_func - dc thực thi
	def wrapper_func(request, *args, **kwargs): 
		if request.user.is_authenticated: # if user is authenticated, dẫn họ tới trang home chứ ko bắt đăng nhập lại
			return redirect('home')
		else: # if user is NOT authenticated, view_func (VD: login page) sẽ dc gọi
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists(): # check if user is part of a group
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function