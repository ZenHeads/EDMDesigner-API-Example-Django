from django.conf.urls import url

urlpatterns = [
    url(r'^token', 'edm.views.token', name='token'),
    url(r'^generate/(?P<project_id>[a-z\d]+)$', 'edm.views.generate', name='generate'),
    url(r'^', 'edm.views.edm_designer', name='designer'),
]


