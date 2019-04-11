from django.shortcuts import render, redirect
from . import forms
# from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Booking
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from datetime import date

# Create your views here.
def home(request):
    currentEvents = []
    users = []
    event_id = []
    bookingData = Booking.objects.all().order_by('eventStartTime').values()
    registered_users_names = [] 
    for i in bookingData:
      if i['eventStartTime'] > date.today():
        currentEvents.append(i)
        event_id.append(i['created_by_id'])
        user = User.objects.filter(id=i['created_by_id']).first()
        
    registered_users = User.objects.all().values()
    # print(registered_users)
    user_details = {}
    for id in event_id:
      for user in registered_users:
        if id == user['id']:
          print("the username is " + user['username'])
          first = user['first_name']
          last = user['last_name']
          full_name = first + " " + last
          registered_users_names.append(full_name)
          users.append(full_name)
          break

   
    assigned_stewards = []
    # print(registered_users_names)
    # for id in event_id:
    #   user = registered_users_names[id-1]
    #   assigned_stewards.append(user)
      
    # print(assigned_stewards)

    # print(event_id)
    
    return render(request, 'globalkitchenapp/index.html', {'bookingData': currentEvents, 'userData': registered_users_names})

@csrf_exempt
def booking(request):
  data = request.POST
  print(data)
  if(len(data)> 0):
    Booking.objects.create(eventName=data.get('event'), bookerName=data.get('name'), bookerEmailField=data.get('email'), phoneField=data.get('phone'), eventStartTime=data.get('arrive'),eventEndTime=data.get('depart'),numberOfPeople=data.get('numberOfPeople'), comment=data.get('comments'))
    return HttpResponseRedirect('/fullcalender/')
  return render(request, 'globalkitchenapp/booking.html') 

@csrf_exempt
def fullcalender(request):
  if(request.GET):
    dataGet = request.GET
    change = Booking.objects.filter(pk=dataGet.get('pk')).first()
    change.eventName = dataGet.get('event')
    change.bookerName=dataGet.get('name')
    change.bookerEmailField=dataGet.get('email')
    change.phoneField=dataGet.get('phone')
    change.eventStartTime=dataGet.get('arrive')
    change.eventEndTime=dataGet.get('depart')
    change.numberOfPeople=dataGet.get('numberOfPeople')
    change.comment=dataGet.get('comments')
    change.save()

  if(request.POST):
    data = request.POST
    print(data)
    if len(data) > 1:
      Booking.objects.create(eventName=data.get('event'), bookerName=data.get('name'), bookerEmailField=data.get('email'), phoneField=data.get('phone'), eventStartTime=data.get(
          'arrive'), eventEndTime=data.get('depart'), numberOfPeople=data.get('numberOfPeople'), comment=data.get('comments'), created_by=request.user)
    else:
      Booking.objects.filter(pk=data.get('pk')).delete()
    
  bookingData = Booking.objects.all()
  bookingDataStr = serializers.serialize("json", bookingData,cls=DjangoJSONEncoder)
  return render(request, 'globalkitchenapp/fullcalender.html', {'bookingData': bookingDataStr})


def selectable(request):
  return render(request, 'globalkitchenapp/selectable.html')
def about(request):
  return render(request, 'globalkitchenapp/about.html')


def contact(request):
  if request.method == 'POST':
    contact_form = forms.ContactedPeople(request.POST)
    # HttpResponse("we are here")
    if contact_form.is_valid():
      contact_form.save(commit=True)
      return HttpResponseRedirect(reverse('home'))
    else:
      print(contact_form.errors)
      HttpResponse("Form did not save")
  else:
    contact_form = forms.ContactedPeople()
  return render(request, 'globalkitchenapp/contact.html', {'contact_form': contact_form})

def login_user(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    
    if user:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            HttpResponse("Account not active!")
    else:
        print("someone tried to login and failed!")
        print("username: {} and password {}".format(username, password))
        # raise forms.ValidationError('Email já em uso')
        # raise ValidationError("Sorry, that login was invalid. Please try again.")
        messages.error(request,'Sorry, Username or Password Incorrect. Please try again.')
        return redirect('/login/')
        # return render(request, 'globalkitchen/login.html', {"err":"Sorry, that login was invalid. Please try again."})
  else:

     return render(request, 'globalkitchenapp/login.html', {})
def signup(request):
  registered = False
  if request.method == 'POST':
    user_form = forms.UserForm(data=request.POST)

    if user_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()
      registered = True
      login(request, user)
      return HttpResponseRedirect(reverse('home'))
    else:
        print(user_form.errors)
  else:
      user_form = forms.UserForm()

  return render(request, 'globalkitchenapp/signup.html', {'user_form': user_form, 'registered': registered})
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))
