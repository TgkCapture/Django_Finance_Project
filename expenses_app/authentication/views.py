from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error: email already exists'}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric values'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error: username already exists'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(
                        request, 'Password should be at least 6 characters long')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration successful')
                return render(request, 'authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
