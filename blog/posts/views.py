from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post
from .forms import PostForm
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.auth.decorators import login_required 
# Create your views here.

def post_create(request):
	if not request.user.is_authenticated:
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		instance = form.save(commit=False)
		print(instance.title)
		print(instance.content)
		instance.user = request.user
		instance.save()
		messages.success(request, 'Successfully created')
		return HttpResponseRedirect(instance.get_absolute_url())

	messages.success(request, 'Error')	
	context = {
			'title': 'create',
			'form': form,	
	}
	return render(request, 'post_form.html', context)


def post_list(request):
	queryset = Post.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset = Post.objects.all()
	# paginator = Paginator(queryset, 5)

	# if request.method == 'GET':
	# 	page_num = request.GET.get('page')

	# qs = paginator.get_page(page_num)


	paginator = Paginator(queryset, 5)
	
	
	page_num = request.GET.get('page')

	try:
		qs = paginator.page(page_num)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		qs = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		qs = paginator.page(paginator.num_pages)


	context = {
				'title': 'list',
				'objects_list': qs,
		}
	return render(request, 'post_list.html', context)	


def post_detail(request, slug=None):
	qs = get_object_or_404(Post ,slug=slug)
	
	if qs.draft or qs.publish > timezone.now().date():
		if not request.user.is_authenticated:
			raise Http404

	initial_data = {
				'content_type': qs.content_type,
				'object_id': qs.id,
	}

	form = CommentForm(request.POST or None, initial=initial_data)	
	if form.is_valid() and request.user.is_authenticated:
		c_type = form.cleaned_data['content_type']
		cont_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data['object_id']
		cont = form.cleaned_data['content']

		parent_obj = None

		try:
			parent_id = int(request.POST.get('parent'))
		except:
			parent_id = None	

			
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() or parent_qs.count() == 1 :
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
									user=request.user,
									content_type=cont_type,
									object_id=obj_id,
									content=cont,
									parent=parent_obj
								)

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	if request.user == qs.user :
		delete_stat = True
	else:
		delete_stat = False	 	
		
	context = {
			'title': 'detail',
			'object': qs,
			'comments': qs.comments,
			'form': form,
			'delete_stat': delete_stat
		}
	return render(request, 'post_detail.html', context)	


def post_update(request, slug=None):
	if not request.user.is_authenticated:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)

	if form.is_valid():
		instance = form.save(commit=False)
		print(instance.title)
		print(instance.content)
		instance.save()
		messages.success(request, 'Successfully updated')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
				'title': 'update',
				'form': form,	
	}
	return render(request, 'post_form.html', context)	



def post_delete(request, slug=None):
	if not request.user.is_authenticated:
		raise Http404

		instance.user = request.user
	obj = get_object_or_404(Post, slug=slug)
	obj.delete()
	return HttpResponseRedirect(reverse('list'))	