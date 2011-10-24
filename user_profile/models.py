#Django imports
from django.db import models
from django import forms
from django.forms import ModelForm


#My imports
from django.contrib.auth.models import User


class Trip(models.Model):
    user = models.ForeignKey(User)
    destination = models.CharField(max_length=150)
    start_time = models.DateField(verbose_name="Start time(mm/dd/yyyy)")
    end_time = models.DateField(verbose_name="End time(mm/dd/yyyy)")
    #Water type can be river, lake, creek++
    water_type = models.CharField(max_length=150)
    comment = models.TextField()
    
    def __unicode__(self):
        #Displays destination
        #number of days the trip lasted and when it started.
        time_delta = self.start_time - self.end_time
        num_days = time_delta.days
        return '%s -- %s days -- started: %s' %(self.destination,
                                                num_days,
                                                self.start_time
                                               )


class Fish(models.Model):
    #Contains info about fish
    trip = models.ForeignKey(Trip)
    fish_type = models.CharField(max_length=100)
    weight = models.IntegerField(verbose_name="Weight in gram")
    length = models.IntegerField(verbose_name="length in cm")
    #Fly, spinner...
    lure = models.CharField(max_length=100)
    comment = models.TextField()


class TripForm(ModelForm):
    #Class created a django form out of a Trip object
    class Meta:
        #User is handled in user_profile.view
        exclude = ('user',)
        model = Trip

    
    def clean_end_time(self):
        #get cleaned data
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data['start_time']
        if end_time < start_time:
            #User entered a start date after end date
            raise forms.ValidationError('Start time must be before end time')
        return end_time
        
        
class FishForm(ModelForm):
    #Class created a django form out of a Fish object
    class Meta:
        model = Fish