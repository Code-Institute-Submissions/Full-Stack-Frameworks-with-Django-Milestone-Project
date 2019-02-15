from django.shortcuts import render, reverse, redirect
from django.contrib import auth, messages
from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect(reverse('login'))

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('profile'))
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                                password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have been logged in")
                return redirect(reverse('profile'))
            else:
                login_form.add_error(None, "The username or password is incorrect")

    else:
        login_form = LoginForm()
    
    return render(request, 'login.html', {"login_form": login_form})

def register(request):

    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)
        
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username = request.POST['username'], password = request.POST['password1'])
            user_group = Group.objects.get(name='SupportUsers')
            user_group.user_set.add(user)

            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You have been registered')
                return redirect(reverse('profile'))

            else:
                messages.error(request, "We are unable to register your account at the moment")

    else:
        registration_form = RegistrationForm()

    return render(request, 'register.html', {"registration_form": registration_form})

def profile(request):
    user = User.objects.get(email=request.user.email)
    print(type(user))
    print(user.username)
    return render(request, 'profile.html', {'profile': user})