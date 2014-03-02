# Create your views here.
from django.shortcuts import HttpResponse,render_to_response, RequestContext,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Project,Photo,Video
from django.shortcuts import render
def home(request):
	return render_to_response("home.html",context_instance=RequestContext(request))
	
def about(request):
	return render_to_response("about.html",context_instance=RequestContext(request))
	
def projects(request):
	projects=Project.objects.all()
	return render(request,'projects.html',{'projects':projects,})
	#return render_to_response("projects.html",context_instance=RequestContext(request))
	
def resources(request):
	return render_to_response("resources.html",context_instance=RequestContext(request))
	
def blog(request):
	return render_to_response("blog.html",context_instance=RequestContext(request))

def blogpost(request):
	return render_to_response("blog-post.html",context_instance=RequestContext(request))
	
def contact(request):
	return render_to_response("contact.html",context_instance=RequestContext(request))
	
def projectinfo(request):
	return render_to_response("projectinfo.html",context_instance=RequestContext(request))
