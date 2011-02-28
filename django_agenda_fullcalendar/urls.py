from django.conf.urls.defaults import *
from django.conf import settings

from myagenda.views import current_month_view, create_event, show_event, del_event

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(r'^$', current_month_view, name="myagenda_current_month_view"),
    url(r'^event/create/', create_event, name="myagenda_create_event"),
    url(r'^event/(?P<slug>[-\w]+)/$', show_event, name='myagenda_show_event'),
    url(r'^event/(?P<slug>[-\w]+)/del/$', del_event, name='myagenda_del_event'),
    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )