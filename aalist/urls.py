from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aalist.views.home', name='home'),
    # url(r'^aalist/', include('aalist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/', 'aalist.views.signup', name='signup'),
    url(r'^login/', 'aalist.views.login', name='login'),
    url(r'^logout/', 'aalist.views.logout', name='logout'),
    url(r'^users/', 'aalist.views.users', name='users'),
    url(r'^$', 'aalist.views.hello', name='hello'),
)
