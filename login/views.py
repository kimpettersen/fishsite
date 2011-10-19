#Contains User registration, login, logout and other related topics
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import simplejson
from django.contrib.auth.forms import UserCreationForm

#TODO-Set up cache for the password checker. 

def register(request):
    #Uses django's default UserCreationForm form. Renders 'user_profile.index' 
    #with success message if registration went OK.
    #If form is not validated or something is missing will it display an error
    #Message 
    info_string = ''    
    if request.method == 'POST':
        formset = UserCreationForm(request.POST)
        if formset.is_valid():
            formset.save()         
            data = {'info' : 'Succesfully registered'}
            return render(request, 'user_profile/index.html', data)
        else:
            info_string = 'Please fill in the right information'
    else:
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
    
    #Tries to get username and password from POST.
    #returns in silence to the login window
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return show_login_form(request)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'user_profile/profile.html')
        else:
            error_string = 'User is deactivated'
    else:
        error_string = 'Wrong username or password'
    return render(request, 'login/login.html', {'error' : error_string})
