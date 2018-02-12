from django.shortcuts import render, redirect
from django.contrib.auth import (
		get_user_model,
		login,
		logout,
		authenticate
	) 
from .forms import LoginForm, RegisterForm
# Create your views here.

def login_view(request):
	form = LoginForm(request.POST or None)
	next = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']

		user = authenticate(username=username, password=password)
		login(request, user=user)
		if next:
			return redirect(next)
		return redirect('/')

	context = {
		'title': 'Login',
		'form': form
	}
	return render(request, 'form.html', context)


def register_view(request):
	
	form = RegisterForm(request.POST or None)
	next = request.GET.get('next')
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect('/')

	context = {
		'title': 'Register',
		'form': form,
	}
	return render(request, 'form.html', context)

def logout_view(request):
	logout(request)
	return redirect('/')		