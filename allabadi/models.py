from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Uid(models.Model):
    
    uid = models.IntegerField( primary_key=True) 
    mac = models.TextField()   
    mac_hash = models.TextField() 
    rollno = models.IntegerField()
    batch = models.TextField()
    access = models.IntegerField()
    email = models.EmailField()
    type = models.TextField()

    def get_absolute_url(self):

        return reverse('person-list', kwargs={'pk': self.uid})


class logs(models.Model):
	
    id = models.AutoField(primary_key=True)
    device = models.IntegerField()
    ts = models.DateTimeField()
    label = models.CharField(max_length=30)
    type = models.IntegerField()
    client_id = models.IntegerField()




