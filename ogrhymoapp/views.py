from django.shortcuts import render, redirect, reverse

from django.core.mail import BadHeaderError, send_mail

from django.http import HttpResponse,HttpResponseRedirect

from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.forms import UserCreationForm

from django.core.mail import EmailMessage

from django.conf import settings

from django.template.loader import render_to_string

from .models import *



from .forms import *

# Create your views here.

def home(request):
	return render(request, 'ogrhymoapp/home.html')

def about(request):
	return render(request, 'ogrhymoapp/about.html')

def contact(request):
    if request.method == 'GET':
        form= ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name= form.cleaned_data['name']
            email= form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(name, "Investor {} has sent a message saying: {}".format(email, message),email, ['customercare@nsbinvest.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Your message has been sent successfully')
    return render(request, "ogrhymoapp/contact.html", {'form': form})

def promotion(request):
	return render(request, 'ogrhymoapp/promotion.html')

def signup(request):

	if request.user.is_authenticated:
		return HttpResponse('You are signed in already. However if you want to create a new account, please signout and do so.')

	else:

		form= CreateUserForm()

		if request.method=='POST':
			form= CreateUserForm(request.POST)
			if form.is_valid():
				user= form.save()
				username= form.cleaned_data.get('username')
				firstname= form.cleaned_data.get('firstname')
				lastname= form.cleaned_data.get('lastname')
				email= form.cleaned_data.get('email')
				messages.success(request, "An account has been created for " + username + " please check your mail or spam folder. ")

				Customer.objects.create(
					user= user,
					firstname= firstname,
					email= email,
					)

				return redirect('loginpage')

			else:
				return HttpResponse('sorry something went wrong, please try again. This could be because a particular user with these details already exists.')

	context={'form': form}

	return render(request, 'ogrhymoapp/signup.html', context)

def loginpage(request):

	if request.user.is_authenticated:
		return HttpResponse('You are already logged in!')

	else:
		if request.method == "POST":
			username= request.POST.get('username')
			password= request.POST.get('password')

			user= authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')

			else:
				messages.error(request, "username or password is incorrect")


		context={}

		return render(request, "ogrhymoapp/login.html", context)

def logoutuser(request):
	logout(request)
	return redirect('loginpage')

def dashboard(request):
	if request.user.is_authenticated:
		print('I am logged in.')

		customer= request.user.customer
		customer.save()
		investments= customer.investment_set.all()

	else:
		return HttpResponse('You are not logged in!')
	context={'customer': customer,'investments': investments }
	return render(request, 'ogrhymoapp/dashboard.html', context)

def deposite(request):
    if request.user.is_authenticated:
        customer= request.user.customer
    else:
        return HttpResponse('You are not logged in!!')

    context= {"customer":customer}
    return render(request, "ogrhymoapp/deposite.html", context)

def requestwithdrawal(request):
    if request.method == 'GET':
        form = RequestForm()
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, "Investor {} has requested a withdrawal of {}".format(from_email, subject),from_email, ['customercare@nsbinvest.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Your withdrawal request has been placed successfully. Please note if you are not on any withdrawal plan, default withdrawal is $50")

    return render(request, "ogrhymoapp/request.html", {'form': form})

def accountSettings(request):

    if request.user.is_authenticated:
        customer= request.user.customer
        form=CustomerForm(instance=customer)
        if request.method=='POST':
            form= CustomerForm(request.POST, request.FILES, instance=customer)
            if form.is_valid():
                form.save()
    else:
        return redirect('/')

    context= {"form":form}
    return render(request, 'ogrhymoapp/account_settings.html', context)


