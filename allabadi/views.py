from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.views.generic import ListView
from allabadi.models import Uid , logs
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
import forms
from django.contrib.auth import logout
import re
from django.views.generic import UpdateView
from datetime import datetime
import random
import json,csv
import pycurl
import StringIO


def homeview(request):
	if (request.user.is_authenticated()):
		logout(request)
		return render(request, 'index.html')

	else:
		return render(request, 'index.html')

def index(request):
	#print("index")
	if (request.user.is_authenticated()):
		return emailcheck(request)
		
	else:
		#print("yaha")
		return render(request, 'index.html')

def emailcheck(request):
	
	#print("check")
	#print(request.user.email)
	match = re.match(r'^[A-Za-z0-9-]+\@iiitd\.ac\.in$', request.user.email)
	if match:	
		return render(request, 'options.html')

	else:
		logout(request)
		return render(request, 'index123.html')
	
	
def logout(request):
	"""Logs out user"""
	auth_logout(request)
	return HttpResponseRedirect('/')


class ListPersonView(ListView):
    model=Uid
    template_name='person_list.html'


class CreatePersonView(CreateView):
   
	form_class = forms.PersonForm
	template_name="person_create.html"

   	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
     		return super(CreatePersonView, self).dispatch(*args, **kwargs)
	
	def form_valid(self, form):
        	person = form.save(commit=False)
        	person.save()        
        	return HttpResponseRedirect(self.get_success_url())


	def get_context_data(self, **kwargs):
		context = super(CreatePersonView, self).get_context_data(**kwargs)
        	context['action'] = reverse('person-create')
		return context

	def get_success_url(self):
	        return reverse('profileview')

class ProfileView(ListView):
	model= Uid	
	template_name="profileview.html"


	def get_context_data(self, **kwargs):
   	    context = super(ProfileView, self).get_context_data(**kwargs)
	    return context


class Options(TemplateView):
	template_name = "options.html"


class FindPersonView(FormView):
	template_name = 'findperson.html'
	form_class = forms.FindPersonForm
	
	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
        	return super(FindPersonView, self).dispatch(*args, **kwargs)

    	def form_valid(self, form):
		if form.is_valid():
    			rollnumber = form.cleaned_data['Roll_number']
			rollnumber = str(rollnumber)
			email= form.cleaned_data['Email']
			email = str(email)
			person_type = form.cleaned_data.get('person_type')
			#person_type = form.cleaned_data['Person_type']
			person_type = str(person_type)
			url= "https://192.168.1.40:9136/su/get?rollno="
			if(email):
				url=url+email
			else:
				url= url + rollnumber
			url = url + "&token=d82132a681be6456903be1f925eec301b8473ef6803286dd92f63abb159ea9a2"
			c = pycurl.Curl()
			c.setopt(pycurl.URL, url)
			c.setopt(pycurl.SSL_VERIFYPEER, 0)
			c.setopt(pycurl.SSL_VERIFYHOST, 0)
			b = StringIO.StringIO()
			c.setopt(pycurl.WRITEFUNCTION, b.write)
			c.setopt(pycurl.FOLLOWLOCATION, 1)
			c.setopt(pycurl.MAXREDIRS, 5)
			c.perform()
			htmlsrc = b.getvalue()	

			json_data=htmlsrc
			data = json.loads(json_data)	
			#print("data")
			#print data

			details={}
			siz1 = len(data["devices"])
			#print("siz1")
			#print siz1
			access=0
			for i in range(0,len(data["devices"])):
				#print ("i")				
				#print i

				uid=data["devices"][i]["uid"]
				access=data["devices"][i]["access"]
				type=data["devices"][i]["device type"]
				uid=data["devices"][i]["uid"]
				#print("access:")
				#print access
				url1= "https://192.168.1.40:9136/client?uid="
				url1= url1+ uid
				#url1= url1+ "6602"
				url1= url1 + "&last=1&token=d82132a681be6456903be1f925eec301b8473ef6803286dd92f63abb159ea9a2"
				c1 = pycurl.Curl()
				c1.setopt(pycurl.URL, url1)
				c1.setopt(pycurl.SSL_VERIFYPEER, 0)
				c1.setopt(pycurl.SSL_VERIFYHOST, 0)
				b1 = StringIO.StringIO()
				c1.setopt(pycurl.WRITEFUNCTION, b1.write)
				c1.setopt(pycurl.FOLLOWLOCATION, 1)
				c1.setopt(pycurl.MAXREDIRS, 5)
				c1.perform()
				htmlsrc1 = b1.getvalue()	

				json_data1=htmlsrc1
				data1 = json.loads(json_data1)	
				#print("data1")
				#print data1
				details1={}

				siz = len(data1["log entries"])
				#print("siz")
				#print siz
				if( siz > 0):
					maxto = data1["log entries"][0]["to"]
					maxfrom = data1["log entries"][0]["from"]
					#details1["to"]=data1["log entries"][0]["to"]
					#details1["from"]=data1["log entries"][0]["from"]
					#details1["device_id"]=data1["log entries"][0]["device_id"]
				  	#details1["location"]=data1["log entries"][0]["location"]
					locat = data1["log entries"][0]["location"]
					#print("loc: ")
					#print(data1["log entries"][0]["location"])

					for j in range(0,len(data1["log entries"])) :
						if( (data1["log entries"][j]["to"]) > maxto and (data1["log entries"][j]["from"] > maxfrom)  ):	
							 #details1["to"]=data1["log entries"][j]["to"]
							 #details1["device_id"]=data1["log entries"][j]["device_id"]
							 #details1["from"]=data1["log entries"][j]["from"]
							 locat = data1["log entries"][j]["location"]
							 
					#print("access yaha:")
					#print access

					if int(access)==0:
						details1["location"]="This person does not want to be located."
					

					elif int(access)==1:
						details1["location"]="This person does not want to be located."
					
					elif int(access)==2:
						list1=locat.split(':')
						wing=list1[0]
						loc=list1[1]		
						details1["location"]=(str(wing)).upper()+" Wing , "+str(loc)
	

					elif int(access)==3:
						list1=locat.split(',')
					 	list2=list1[0].split(':')
					     	wing=list2[0]
						loc=list2[1]
						list3=list1[1].split(':')
						floor=list3[0]	
					 	details1["location"]="Floor: "+str(floor)+", "+str(loc)
						
					
					
					elif int(access)==4:
						list1=locat.split(',')
						list2=list1[0].split(':')
						loc=list2[1]
						list3=list1[1].split(':')
						floor=list3[1]
						list4=list1[2].split(':')
						wing=list4[1]
						details1["location"]="Floor: "+str(floor)+", "+str(wing)+" Wing, "+str(loc)
						

					elif int(access)==5:
						list1=locat.split(',')
						list2=list1[0].split(':')
						loc=list2[1]
						list3=list1[1].split(':')
						floor=list3[1]
						list4=list1[2].split(':')
						wing=list4[1]
						details1["location"]="Floor: "+str(floor)+", "+str(wing)+" Wing, "+str(loc)
						
					
					else:
						details1["location"]="This person does not want to be located. "
					
				
					

					
					


			template = get_template('person_locinfo.html')
	    		context = RequestContext(self.request, {
			'details': details1,
    			})
    			return HttpResponse(template.render(context))
				
	def get_context_data(self, **kwargs):
		context = super(FindPersonView, self).get_context_data(**kwargs)
        	context['action'] = reverse('find-person')
		return context




class AddDeviceView(CreateView):
	
	form_class = forms.AddDeviceForm
	template_name="add-device.html"

   	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
     		return super(AddDeviceView, self).dispatch(*args, **kwargs)
	
	def form_valid(self, form):
				
		person = form.save(commit=False)
		person.email = self.request.user.email
	#insert rollno to uid function here		
		person.uid= random.randint(1,10000000)
	#insert mac to mac_hash function here		
		person.mac_hash="abcd"
        	person.save()             
        	return HttpResponseRedirect(self.get_success_url())


	def get_context_data(self, **kwargs):
		context = super(AddDeviceView, self).get_context_data(**kwargs)
        	context['action'] = reverse('add-device')
		return context

	def get_success_url(self):
	        return reverse('optionsview')



class SelectDeviceListView(FormView):
	
	data= None	

	@method_decorator(login_required)
    	def dispatch(self, *args, **kwargs):
        	return super(SelectDeviceListView, self).dispatch(*args, **kwargs)
    	
	template_name = 'updaterollno.html'
	form_class = forms.updaterollnoForm

	
		
				
	def get_context_data(self, **kwargs):
		context = super(SelectDeviceListView, self).get_context_data(**kwargs)
        	context['action'] = reverse('select-device')
		return context
	
		
	def form_valid(self, form):
		if form.is_valid():
    			access = form.cleaned_data['Access_level']
			access = str(access)
			#rollno = form.cleaned_data['Roll_number']
			#rollno = str(rollno)
			#email= form.cleaned_data['Email']
			#email = str(email)

			email = self.request.user.email
			url= "https://192.168.1.40:9136/su/get?rollno="
			url=url+email
			#if(email):
			#	url=url+email
			#else:
			#	url= url + rollno
			url = url + "&token=d82132a681be6456903be1f925eec301b8473ef6803286dd92f63abb159ea9a2"
			c = pycurl.Curl()
			c.setopt(pycurl.URL, url)
			c.setopt(pycurl.SSL_VERIFYPEER, 0)
			c.setopt(pycurl.SSL_VERIFYHOST, 0)
			b = StringIO.StringIO()
			c.setopt(pycurl.WRITEFUNCTION, b.write)
			c.setopt(pycurl.FOLLOWLOCATION, 1)
			c.setopt(pycurl.MAXREDIRS, 5)
			c.perform()
			htmlsrc = b.getvalue()	
			json_data=htmlsrc
			data = json.loads(json_data)	
	
			#print data["devices"][0]["uid"]

			detailed={}
			for i in range(0,len(data["devices"])):
				detailed[i]=data["devices"][i]["uid"]


			for i in range(0,len(data["devices"])):
				url=""
				url=url+"https://192.168.1.40:9136/su/put?uid="
				url=url+data["devices"][i]["uid"]		
				url=url+"&access="
				url=url+access				
				url=url+"&token=d82132a681be6456903be1f925eec301b8473ef6803286dd92f63abb159ea9a2"
				c = pycurl.Curl()
				c.setopt(pycurl.URL, url)
				c.setopt(pycurl.SSL_VERIFYPEER, 0)
				c.setopt(pycurl.SSL_VERIFYHOST, 0)
				b = StringIO.StringIO()
				c.setopt(pycurl.WRITEFUNCTION, b.write)
				c.setopt(pycurl.FOLLOWLOCATION, 1)
				c.setopt(pycurl.MAXREDIRS, 5)
				c.perform()
				htmlsrc = b.getvalue()			

			#detail = Uid.objects.get(rollno = rollnumber)
			#details = logs.objects.filter(client_id = detail.uid)
			#print(details)
			return HttpResponseRedirect(self.get_success_url())
	
	def get_success_url(self):
	        return reverse('optionsview')	


class UpdateDeviceView(UpdateView):

    template_name = 'devicesview.html'
    form_class = forms.EditForm

    def get_success_url(self):
        return reverse('person-list')

    def get_context_data(self, **kwargs):

        context = super(UpdateDeviceView, self).get_context_data(**kwargs)
        context['action'] = reverse('device-edit',
                                    kwargs={'pk': self.get_object().uid})

        return context


class CreateLogsView(CreateView):
   
	form_class = forms.InsertLog
	template_name="logs_create.html"

   	@method_decorator(login_required)
  	def dispatch(self, *args, **kwargs):
     		return super(CreateLogsView, self).dispatch(*args, **kwargs)
	
	def form_valid(self, form):
        	person = form.save(commit=False)
		
        	person.save()        
        	return HttpResponseRedirect(self.get_success_url())


	def get_context_data(self, **kwargs):
		context = super(CreateLogsView, self).get_context_data(**kwargs)
        	context['action'] = reverse('logs')
		return context

	def get_success_url(self):
	        return reverse('person-list')





