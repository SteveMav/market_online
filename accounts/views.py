from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import LoginForm, RegistrationForm
from validate_email_address import validate_email
from django.shortcuts import redirect
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.utils.translation import gettext as _




# Create your views here.
def login(request):
    
    pass

# User registration view
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        if validate_email(request.POST.get('email')):
            form = RegistrationForm(request.POST)
            if form.is_valid():
                try:
                    # Create user, send welcome email, and log in
                    user = form.save()
                    # Use ThreadPoolExecutor to run send_welcome_email with a timeout
                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #     future = executor.submit(send_welcome_email, user)
                    #     try:
                    #         future.result(timeout=5)  # Wait for 5 seconds
                    #     except concurrent.futures.TimeoutError:
                    #         # If it takes more than 5 seconds, we just continue
                    #         pass
                    
                    login(request, user)
                    messages.success(request, _('Account created successfully!'))
                    return redirect('main:index')
                except Exception as e:
                    messages.warning(request, _('Error creating account:')) 
            else:
                # Handle form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        if 'username' in error:
                            messages.warning(request, _('Username already taken, please choose another.'))
                            return render(request, 'accounts/register.html', {'form': form})
                        elif 'email' in error:
                            messages.warning(request, _('Email address already in use, please choose another.'))
                            return render(request, 'accounts/register.html', {'form': form})
                        elif 'password' in error:
                            messages.warning(request, _('Password error: ') + _(error))
                            return render(request, 'accounts/register.html', {'form': form})
                        else:
                            messages.warning(request, _('erreur au champ mot de passe: {error}').format(field=field, error=_(error)))
                return render(request, 'accounts/register.html', {'form': form})
        else:
            messages.warning(request, _('The email address is not valid.'))
            return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})

