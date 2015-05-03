from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import allabadi.views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^$', allabadi.views.index, name='home'),
    
    url(r'^home', allabadi.views.homeview , name='homeview'),
    
    #url(r'^welcome/', allabadi.views.welcome, name='welcome'),
    
    url(r'^logout/', allabadi.views.logout, name='logout'),

    url(r'^echeck/', allabadi.views.emailcheck, name='echeck'),
    
    url(r'^create', allabadi.views.CreatePersonView.as_view(),
        name='person-create',),

    url(r'^profileview', allabadi.views.ProfileView.as_view(),
        name='profileview',),

    url(r'^options', allabadi.views.Options.as_view(),
        name='optionsview',),

    url(r'^findperson', allabadi.views.FindPersonView.as_view(),
        name='find-person',),
    
    url(r'^selectdevice', allabadi.views.SelectDeviceListView.as_view(),
        name='select-device',),

    url(r'^adddevice', allabadi.views.AddDeviceView.as_view(),
        name='add-device',),

    url(r'^edit/(?P<pk>\d+)/$', allabadi.views.UpdateDeviceView.as_view(),
        name='device-edit',),

    
    

    url('', include('social.apps.django_app.urls', namespace='social'))



)



urlpatterns += staticfiles_urlpatterns()

