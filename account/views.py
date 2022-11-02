from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login as dj_login
from django.contrib import auth
from django.contrib import messages

def signup(request):
    # if this is a POST request we need to process the form data
    template = 'register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.contact_number_self = form.cleaned_data['contact_number_self']
                user.save()
                registred=True

                # redirect to accounts page:
                messages.success(request, ('User has been registerd successfully '))
                return redirect('login')

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

def login(request):
    if request.method == 'POST':
        # Process the request if posted data are available
        email = request.POST['email']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=email, password=password)
        if user is not None:
            # Save session as cookie to login the user
            dj_login(request, user)
            # Success, now let's login the user.
            messages.success(request, ('User has been login successfully '))
            return redirect('/')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')