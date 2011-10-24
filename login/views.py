#Contains User registration, login, logout and other related topics
#Django imports
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import simplejson
from django.contrib.auth.forms import UserCreationForm

#TODO -Set up cache for the password checker. 

def register(request):
    #Register a user. Uses djangos built in UserCreationForm
    
    info_string = ''    
    if request.method == 'POST':
        #User submitted a form
        formset = UserCreationForm(request.POST)
        if formset.is_valid():
            #Form is valid and will be saved.
            formset.save()         
            data = {'info' : 'Succesfully registered'}
            return show_login_form(request)
        else:
            #Form was invalid.
            info_string = 'Please fill in the right information'
    else:
        #Creates an empty form
        formset = UserCreationForm()
    data = {'formset' : formset, 'info' : info_string}
    return render(request, 'login/registration.html', data)


def check_username_availability(request, username):
    #Used to check if a username is available. Returns a JSON object with
    #key: 'user_exists'. Returns True if user exists 
    
    message = {}
    try:
        #Looking for a user with the given username. This will happen very
        #often.
        user = User.objects.get(username__exact=username)
        message = {'user_exists' : True}
    except:
        #Raises an MultiDictValue exception if user does not exist.
        #i.e the username is available.
        message = {'user_exists' : False}
    json = simplejson.dumps(message)
    return HttpResponse(json)


def show_login_form(request):
    #method to display a basic login form
    return render(request, 'login/login.html')


def log_in(request):
    # Loggs a user in if the user is authenticated, exists and is active.
    #Redirects to user_profile.profile on success.
    #login.show_login_form if failure

    try:
        #get the usernames
        username = request.POST['username']
        password = request.POST['password']
    except:
        #Usernames where not submitted, displays the login window
        return show_login_form(request)
    #Authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        #User exists
        if user.is_active:
            #The user is authentcated and active will be logged in.
            login(request, user)
            #returns to index site
            return render(request, 'user_profile/index.html')
        else:
            #Deactivated user
            error_string = 'User is deactivated'
    else:
        #Wrong username or password
        error_string = 'Wrong username or password'
    return render(request, 'login/login.html', {'error' : error_string})

    
def log_out(request):
    #If the user is logged in, the user will be loged out.
    
    info_string = ''
    if request.user.is_authenticated():
        # loggs out the user
        logout(request)
        info_string = 'Succesfully logged out..'
    else:
        #user wasn't logged in in the first place
        info_string = 'You must be logged in to log out..'
    data = {'info' : info_string}
    return render(request, 'user_profile/index.html', data)