from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request) :
	contact_list = Post.objects.all()
	paginator = Paginator(contact_list, 5) # Show 25 contacts per page
	page_number = 'page'
	page = request.GET.get(page_number)
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		contacts = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		contacts = paginator.page(paginator.num_pages)
	context = {	
		"title" : "List",
		"page_number" : page_number,
		"queryset" : contacts
	}
	return render(request, "base.html", context)

def post_create(request) :
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid() :
		instance = form.save(commit = False)
		instance.save()
		# message success
		messages.success(request, "Successfully created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : form
	}
	return render(request, "post_form.html", context)
from urllib import quote_plus
def post_detail(request, slug = None) : #retrieve
	example = get_object_or_404(Post, slug = slug)
	share_link = quote_plus(example.content)
	context = {
		"title" : example.title,
		"example" : example,
		"share_link" : share_link
	}
	return render(request, "post_detail.html", context)
def post_update(request, slug = None) :
	example = get_object_or_404(Post, slug = slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = example)
	if form.is_valid() :
		instance = form.save(commit = False)
		instance.save()
		# message success
		messages.success(request, "<a href = '#'>Item</a> Saved!", extra_tags = 'html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title" : example.title,
		"example" : example,
		"form" : form,
	}	
	return render(request, "post_form.html", context)	

def post_delete(request, slug = None) :
	instance = get_object_or_404(Post, slug = slug)
	instance.delete()
	messages.success(request, "Successfully deleted!")	
	return redirect("webapp:list")	
