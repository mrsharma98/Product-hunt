from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Product
# Create your views here.

def home(request):
    products = Product.objects
    return render(request, 'products/home.html', {'products':products})


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

            return redirect('/products/'+str(product.id))


        else:
            return render(request, 'products/create.html', {'error':'All fields are required.'})

    else:
        return render(request, 'products/create.html')



def detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    return render(request, "products/detail.html", {'product':product})


@login_required(login_url="/accounts/signup")
# if a anonymous user tries to upvote then it will take it to
# the signup page as mentioned above
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()

        return redirect('/products/'+str(product.id))


@login_required(login_url="/accounts/signup")
def upvotedd(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()

        return redirect('home')
