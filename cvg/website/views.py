# Create your views here.
from django.shortcuts import HttpResponse,render_to_response, RequestContext,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Project,Photo,Video
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def home(request):
	return render_to_response("home.html",context_instance=RequestContext(request))
	
def about(request):
	return render_to_response("about.html",context_instance=RequestContext(request))
	
def projects(request):

	project_list=Project.objects.all()
	paginator = Paginator(project_list, 1) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		projects = paginator.page(page)
	except PageNotAnInteger:
		projects = paginator.page(1) # If page is not an integer, deliver first page.
	except EmptyPage:
		projects = paginator.page(paginator.num_pages)
    
        # If page is out of range (e.g. 9999), deliver last page of results.
        
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
	
def projectinfo(request,project_id):
	project=Project.objects.get(id=project_id)
	images=project.imag.all()
	videos=project.videos.all()
	return render(request,"projectinfo.html",{'project':project,'images':images,'videos':videos})
