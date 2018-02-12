from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']

		
		#user_qs = User.objects.filter(username=username)
		#if user_qs.count() == 1:
		#	user = user_qs.first()

		if username and password:
			user = authenticate(username=username, password=password)	
			if not user:
				raise forms.ValidationError('This User does not exist')

			if not user.check_password(password):	
				raise forms.ValidationError('Wrong Password')

			if not user.is_active:
				raise forms.ValidationError('User is not active')
		return super(LoginForm, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
	email = forms.EmailField(label="Email")
	email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
			'password2',
		]					

	def clean_email2(self, *args, **kwargs):
		email = self.cleaned_data['email']
		email2 = self.cleaned_data['email2']

		if email != email2:
			raise forms.ValidationError('Email not Matching')

		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError('Email already Exist')

		return email	


	def clean_password2(self, *args, **kwargs):
		password = self.cleaned_data['password'] 
		password2 = self.cleaned_data['password2']

		if password2 != password:
			raise forms.ValidationError('Password not Matching')		 	

		return password2	