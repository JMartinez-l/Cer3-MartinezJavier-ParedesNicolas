from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Formulario(forms.Form):
    # Define your form fields
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email