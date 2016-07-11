from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    first_part = instance.title.split(' ');
    return '%s/%s' %(first_part[0], filename)

class Post(models.Model):
	title = models.CharField(max_length = 120)
	content = models.TextField()
	updated = models.DateField(auto_now = True, auto_now_add = False)
	timestamp = models.DateField(auto_now = False, auto_now_add = True)
	slug = models.SlugField(unique = True)
	image = models.ImageField(upload_to = user_directory_path, 
			null = True, blank = True, 
			height_field = "height_field", 
			width_field = "width_field")
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)


	def __unicode__(self) :
		return self.title
	def __str__(self) :
		return self.title		
	def get_absolute_url(self) :
		return reverse("webapp:detail", kwargs={"slug": self.slug})	
	class Meta:
		ordering = ["-timestamp", "-id"]

import string 
import random

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def pre_save_func(sender, instance, *args, **kwargs):
	slug = slugify(instance.title)
	isExist = Post.objects.filter(slug=slug).exists()
	if isExist:
		slug = slug + "-" + id_generator();
	instance.slug = slug

pre_save.connect(pre_save_func, sender = Post)