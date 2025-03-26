from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import RegistrationForm, LoginForm


class Accounts(View):
    def register(self, request):
        form = RegistrationForm()

        if request.method == 'POST':
            form = RegistrationForm(request.POST)

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('main:index')
                else:
                    messages.error(request, 'Error logging in after account creation.')
            else:
                # Handle form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, 'Error in field {}: {}'.format(field, error))

        return render(request, 'accounts/register.html', {'form': form})

    def login(self, request):
        form = LoginForm()

        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('main:index')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                # Handle form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, 'Error in field {}: {}'.format(field, error))

        return render(request, 'accounts/login.html', {'form': form})


    def deconnect(self, request):
        logout(request)
        return redirect('main:index')

