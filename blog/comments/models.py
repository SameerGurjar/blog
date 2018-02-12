from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# Create your models here.

class CommentManager(models.Manager):
	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = instance.id
		qs = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
		return qs	

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = CommentManager()

	def __str__(self):
		return str(self.user.username)

	class Meta:
		ordering = ['-timestamp']	

	@property	
	def is_parent(self):
		if self.parent is not None:
			return True
		return False

	def children(self):
		return Comment.objects.filter(parent=self)	