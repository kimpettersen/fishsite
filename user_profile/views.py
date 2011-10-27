#the app user_profile contains all logic that have something to do with an
#individual user. As in: manage your own Trips and Fish, see your own profile,
#and generall statistic.

#django imports
from django.shortcuts import render
from django.forms.models import modelformset_factory
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#My imports
from user_profile.models import Trip, Fish, TripForm, FishForm


def index(request):
    #Returns an index page that currently contains all navigation. 
    return render(request, 'user_profile/index.html')


@login_required
def add_trips(request):
    info_string = ''
    if request.method == 'POST':
        #User submitted a form, create one out of the request
        form = TripForm(request.POST)
        if form.is_valid():
            #Form is valid, call function to add user to the form
            form = add_user_to_form(request, form)
            #Go to the index site.
            return render(request, 'user_profile/index.html', { 'info' : 'You saved a Trip' })
        else:
            #Form is not valid
            info_string = 'The form did not validate. Please try again'
    else:
        #Requests empty form
        form = TripForm()    
    
    #Data contains either an empty form or a form with marked errors, the html form action, 
    #The name of the form and an error message if there is a reason to display one.
    data = {'form' : form,
            'action' : '/user_profile/add_trips',
            'form_name' : 'Trip',
            'error' : info_string,
            }
    return render(request, 'user_profile/form.html', data)

    
@login_required    
def add_fish(request):
    #Creates a form from models.FishForm
    form = FishForm()
    info_string = ''
    if request.method == 'POST':
        #User submitted a form, create one out of the request
        form = FishForm(request.POST)
        if form.is_valid():
            #Form is valid, call function to add user to the form
            form = add_user_to_form(request, form)
            #Go to the index site.
            return render(request, 'user_profile/index.html', { 'info' : 'You saved a Fish' })
        else:
            #form is not valid
            info_string = 'The form did not validate. Please try again'
    else:
        #Requests empty form
        form = FishForm()
        #Displays only trips for the current user
        form.fields['trip'].queryset = Trip.objects.filter(user = request.user)

    #Data contains either an empty form or a form with marked errors, the html form action, 
    #The name of the form and an error message if there is a reason to display one.
    data = {'form' : form,
            'action' : '/user_profile/add_fish',
            'form_name' : 'Fish',
            'info' : info_string,
            }
    return render(request, 'user_profile/form.html', data)


@login_required
def add_user_to_form(request, form):
    form = form.save(commit=False)
    #add the user to the current form
    form.user = request.user
    #Save the form
    form.save()
    return form


@login_required
def profile(request):
    #Get list of all trips for the current user
    my_trips = Trip.objects.filter(user = request.user)
    #Get all the fish for current user
    my_fish = []
    for trip in my_trips:
        #For all the trips in the list get all of the fish
        fish_list = Fish.objects.filter(trip = trip)
        if fish_list:
            #appends the fish list to the list of fish
            my_fish.append(fish_list)
    print my_fish
    #render it.
    data = {'my_trips' : my_trips, 'my_fish' : my_fish }
    return render(request, 'user_profile/profile.html', data )
