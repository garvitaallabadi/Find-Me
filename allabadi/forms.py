from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from allabadi.models import Uid , logs

TITLE_CHOICES = (
    ('Student', 'Student'),
    ('Faculty', 'Faculty'),
    ('Staff', 'Staff'),
)
class PersonForm(forms.ModelForm):
    class Meta:
        model = Uid
        

class AddDeviceForm(forms.ModelForm):    

	class Meta:
	        model = Uid
		fields = ['rollno', 'batch', 'access' , 'mac' , 'type' ]

class FindPersonForm(forms.Form):
    Roll_number = forms.IntegerField(required=False)
    Email = forms.CharField(required=False)
    Person_type = forms.CharField(widget=forms.Select(choices=TITLE_CHOICES))

class updaterollnoForm(forms.Form):
    #Roll_number = forms.IntegerField(required=False)
    #Email = forms.CharField(required=False)
    Access_level = forms.IntegerField()

class EditForm(forms.ModelForm):

      class Meta:
        model = Uid


class InsertLog(forms.ModelForm):
	
	class Meta:
        	model = logs
		


