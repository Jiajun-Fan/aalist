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
    url(r'^user/signup/', 'aalist.user.signup'),
    url(r'^user/login/', 'aalist.user.login'),
    url(r'^user/logout/', 'aalist.user.logout'),
    url(r'^user/users/', 'aalist.user.users'),
    url(r'^user/info/', 'aalist.user.info'),
    url(r'^group/create/', 'aalist.group.createGroup'),
    url(r'^group/join/', 'aalist.group.joinGroup'),
    url(r'^group/opt/', 'aalist.group.optGroup'),
    url(r'^$', 'aalist.user.hello'),
)
