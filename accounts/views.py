from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm
from validate_email_address import validate_email
from django.utils.translation import gettext as _

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if not validate_email(request.POST.get('email')):
            messages.warning(request, _('The email address is not valid.'))
        elif form.is_valid():
            try:
                # Create user
                user = form.save()
                # Authenticate and log in the user
                login(request, user)
                messages.success(request, _('Account created successfully!'))
                return redirect('main:index')
            except Exception as e:
                messages.warning(request, _('Error creating account: ') + str(e))
        else:
            # Handle form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    if 'username' in error:
                        messages.warning(request, _('Username already taken, please choose another.'))
                    elif 'email' in error:
                        messages.warning(request, _('Email address already in use, please choose another.'))
                    elif 'password' in error:
                        messages.warning(request, _('Password error: ') + _(error))
                    else:
                        messages.warning(request, _('Error in field {field}: {error}').format(field=field, error=_(error)))

    return render(request, 'accounts/register.html', {'form': form})
