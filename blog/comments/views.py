from django.shortcuts import render, get_object_or_404, Http404
from django.http import HttpResponseRedirect
from .models import Comment
from django.contrib.auth.decorators import login_required 
# Create your views here.


def comment_delete(request, id=None):
	if not request.user.is_authenticated:
		raise Http404

	qs = get_object_or_404(Comment, id=id)

	if not qs.user == request.user and not qs.content_object.user == request.user:
		raise Http404

	redirect_url = qs.content_object.get_absolute_url()
	qs.delete()
	return HttpResponseRedirect(redirect_url)