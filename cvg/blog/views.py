# Create your views here.

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Post
from forms import PostForm, CommentForm
from django.shortcuts import render

#@user_passes_test(lambda u: u.is_superuser)

def blog(request):
	post_list=Post.objects.all().order_by("-created_on")
	paginator = Paginator(post_list, 1) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1) # If page is not an integer, deliver first page.
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request,"blog.html",{'posts':posts,})
	

def add_post(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.author = request.user
		post.save()
		return redirect(post)
	return render_to_response('blog/add_post.html', { 'form': form },context_instance=RequestContext(request))

def blogpost(request, slug):
	post = get_object_or_404(Post, slug=slug)
	
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.post = post
		comment.save()
		return redirect(request.path)
	return render_to_response("blog-post.html",
                              {
                                  'post': post,
                                  'form': form,
                               },
                              context_instance=RequestContext(request))
