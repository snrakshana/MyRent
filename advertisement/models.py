from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver




def upload_location(instance, filename):
	file_path = 'ad/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path


class ADPost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	description 			= models.TextField(max_length=5000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True,default = "180px-FC_Barcelona_(crest).svg.png")
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug 					= models.SlugField(blank=True, unique=True)

	def __str__(self):
		return f"{self.title}"


@receiver(post_delete, sender=ADPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 



def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=ADPost)