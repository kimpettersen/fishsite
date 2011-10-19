from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#urls for user_profile
urlpatterns = patterns('',
    (r'^user_profile/edit_trips', 'user_profile.views.edit_trips'),
    (r'^user_profile/edit_fish', 'user_profile.views.edit_fish'),      
    (r'^$', 'user_profile.views.index'),
    (r'^user_profile/profile', 'user_profile.views.profile'),
    )

#urls for login
urlpatterns += patterns('',
    (r'^login/register', 'login.views.register'),
    (r'^login/loginform', 'login.views.show_login_form'),    
    (r'^login/login', 'login.views.log_in'),
    (r'^login/checkusername/(?P<username>\w+)/$', 
        'login.views.check_username_availability'),
    )

#remove before deploying
urlpatterns += patterns('',    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/kim/fishsite/media/'}),
    )

