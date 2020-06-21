from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import auth
from app_accounts.forms import UserForm, ProfileForm
from django.contrib import messages
from app_accounts.models import Profile

# Create your views here.

def register2(request):
    if request.method == 'POST':
        # The user has info and wants account(sign up)!
        if request.POST['password1'] == request.POST['password2']:
            try:
                # pw are correctly written
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'app_accounts/register2.html', {'error': 'Usuario '+ str(user) + ' ya existe.'})
            except User.DoesNotExist:
                if request.POST['full_name'] and request.POST['phone_number'] and request.POST['address']:
                    new_user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    new_profile = Profile()
                    new_profile.user = new_user #si no funciona,
                    # hay que buscar el usuario asi: user = User.objects.get(username=request.POST['username'])
                    #para luego meter ese user en el new_profile.user
                    new_profile.fullname = request.POST['full_name']
                    new_profile.address = request.POST['address']
                    new_profile.phonenumber = request.POST['phone_number']
                    new_profile.save()

                    auth.login(request, new_user)

                else:
                    return render(request, 'app_accounts/register2.html', {'error': 'Por favor complete todos los campos'})


                return redirect('home')
        return render(request, 'app_accounts/register2.html', {'error': 'Passwords must match !'})
    else:  # User wants to enter info
        return render(request, 'app_accounts/register2.html')



def signup(request):
    if request.method == 'POST':
        # The user has info and wants account(sign up)!
        if request.POST['password1'] == request.POST['password2']:
            try:
                # pw are correctly written
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'app_accounts/signup.html', {'error': 'Username '+ str(user) + ' has already been taken'})

            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
                auth.login(request , user)
                return redirect('home')
        return render(request, 'app_accounts/signup.html', {'error': 'Passwords must match !'})
    else:  # User wants to enter info
        return render(request, 'app_accounts/signup.html')


def login(request):
    if request.method == 'POST':    #if they are trying to log in
        user = auth.authenticate(username=request.POST['username'] , password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'app_accounts/login.html', {'error': 'Username or password is incorrect.'})

    else:   # if they are only trying to view login page
        return render(request, 'app_accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    # TODO - Need to route to homepage , and dont forget to logout
    return render(request, 'app_accounts/signup.html')