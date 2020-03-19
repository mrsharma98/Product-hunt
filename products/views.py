from django.shortcuts import render, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Product
# Create your views here.

def home(request):
    return render(request, 'products/home.html')


# as only authorized and logged in users can only create products
# so we can use decorator to ensure that user who is posting the post
# is logged in currently
# if the user is not loggedin then we will send them to signup ot login page
@login_required
def create(request):

    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:

            product = Product()
            product.title = request.POST['title']
            product.body = request.POST['body']

            # slighty different for url, checking for the valid url
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'https://' + request.POST['url']

            # here request will be FILES and not POST
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']

            product.pub_date = timezone.datetime.now()
            product.hunter = request.user

            product.save()
            # this will insert all the info to the database

            return redirect('home')


        else:
            return render(request, 'products/create.html', {'error':'All fields are required.'})

    else:
        return render(request, 'products/create.html')
