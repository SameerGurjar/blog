from django.conf.urls import url
from .views import comment_delete



urlpatterns = [
	url(r'(?P<id>\d+)/delete/$', comment_delete, name='delete')
]