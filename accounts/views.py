from django.shortcuts import render, redirect

from django.contrib.auth.models import User
# this will give us a User object
from django.contrib import auth


def signup(request):

    if request.method == 'POST':
        # user has enterd his info and wants an account now
        if request.POST['password1'] == request.POST['password2']:
        # this password1 and password2 are the names of our form fields
        # this is for getting the field data
            try:
                user = User.objects.get(username=request.POST['username'])
                # checking whether this username has already been taken by someone else
                return render(request, 'accounts/signup.html', {'error':'Username has already been taken'})

            except User.DoesNotExist:

                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                # creating a User object and saving it to user
                auth.login(request, user)
                # logining the newly created user and redirecting him to the home page
                return redirect('home')

        else:
            # if passwords didn't match
            return render(request, 'accounts/signup.html', {'error':'Password must match'})


    else:
        # user wants to go to sign up page and enter info
        # means he has clicked on signup in navbar
        return render(request, 'accounts/signup.html')

def login(request):

    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        # this will try for the authentication, if it does authenticate
        # it will give us a valid user object
        if user is not None:
            # if we do get a user object
            auth.login(request, user)

            return redirect('home')

        else:
            # if the user is None
            return render(request, 'accounts/login.html', {'error':'Username or passowrd is incorrect'})


    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # in DJango the logout request should be POST
    # as browser like chrome automatically sends get request and load the pages
    # and for this purpose we habe to make a little hidden form attached with logout
    # it will be on base.html as we have logout button there

    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

    return render(request, 'accounts/signup.html')
