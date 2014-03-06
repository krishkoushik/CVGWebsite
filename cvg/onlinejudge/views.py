from django.shortcuts import HttpResponse,render_to_response, RequestContext, HttpResponseRedirect
import re
from django.contrib.auth import authenticate
from django.contrib import auth
from onlinejudge.models import UploadFileForm, CodeToCompile, RequestQueue
import os
import subprocess,shlex
from django.core.files import File
import thread

def process_queue():
	
	while True:
		req=RequestQueue.objects.all()
		print "hello"
		if req.exists():
			for qr in req:
				handle_uploaded_file(qr.codetocompile.id)
				qr.codetocompile.processed="y"
				qr.codetocompile.save()
				qr.delete()
		else:
			break


def handle_uploaded_file(obid):
		
#Compiling code and storing the compile message in object
	code = CodeToCompile.objects.get(id=obid)
	arg=shlex.split("g++ -I/usr/local/include/opencv -I/usr/local/include "+code.fil_e+" /usr/local/lib/libopencv_calib3d.so /usr/local/lib/libopencv_contrib.so /usr/local/lib/libopencv_core.so /usr/local/lib/libopencv_features2d.so /usr/local/lib/libopencv_flann.so /usr/local/lib/libopencv_gpu.so /usr/local/lib/libopencv_highgui.so /usr/local/lib/libopencv_imgproc.so /usr/local/lib/libopencv_legacy.so /usr/local/lib/libopencv_ml.so /usr/local/lib/libopencv_nonfree.so /usr/local/lib/libopencv_objdetect.so /usr/local/lib/libopencv_photo.so /usr/local/lib/libopencv_stitching.so /usr/local/lib/libopencv_superres.so /usr/local/lib/libopencv_ts.so /usr/local/lib/libopencv_video.so /usr/local/lib/libopencv_videostab.so -o output")
	comp = open("compilemessage.txt","wb+")#creating a compile message file
	out=subprocess.call(arg,stderr=comp,shell=False)
	comp.close()
	
	#writing the compile file
	fil = open("compilemessage.txt","r")
	fi = open(str(code.compileoutp),"w")
	fi.write(fil.read())
	fil.close()
	fi.close()
	
	#Running code and storing runtime message
	
	runt = open("runtimemessage.txt","wb+")#creating a runtimemessage file
	runt.close()
	runt = open("mes.txt","wb+")#creating a memcheck message file
	runt.close()
	if out==0 :
		code.compilemessage = 'Successfully Compiled'
		arg=shlex.split("./output")
		runt = open("runtimemessage.txt","wb+")
		out1=subprocess.Popen(arg,stderr=runt,shell=False)
		print out1.pid
		out2=subprocess.Popen(['bash','memcheck.sh',str(out1.pid)],shell=False);
		stdo,stder = out1.communicate()
		stdo,stder = out2.communicate()
		runt.close()
	else :
		code.compilemessage = "Compile Failed"
	
	#writing runtime message (error) to pointed by object
	fil = File(open("runtimemessage.txt","r"))
	fi = open(code.runtimeoutp,"w")
	fi.write(fil.read())
	fil.close()
	fi.close()

	fil = File(open("mes.txt","r"))
	code.runtimemessage = fil.readline()
	fi.close()

	code.save()

	#deleting the temporarily created files
	subprocess.call(["rm","-f","compilemessage.txt","runtimemessage.txt","mes.txt","output"],shell=False)

	
	#To be transferred to another function



def viewsubmission(request,obid):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	
	code=CodeToCompile.objects.get(id=obid)
	if code.user!=request.user:
		return HttpResponseRedirect("/onlinejudge")
	if code.processed=='y':
		
		a = open(code.fil_e,"r")
		b = open(code.compileoutp,"r")
		c = open(code.runtimeoutp,"r")
		return render_to_response('submitted.html', {'fil_e':a,'compile':b,'runtime':c,'code':code},context_instance=RequestContext(request))
	else : 
		return render_to_response('runn.html',{'obid':obid})

submission_message=''
def upload_file(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	l=[]
	submission_message=''
	fo = UploadFileForm(request.POST,request.FILES)
	if request.method == 'POST':
		if fo.is_valid():
			form = request.FILES
			obj,created = CodeToCompile.objects.get_or_create(user=request.user)
			if created is True:
				obj.compilemessage="Compiling..."
				obj.fil_e="media/code/"+str(obj.user.id)+"_"+str(fo.cleaned_data["fil_e"].name)
				obj.compileoutp="media/code/"+str(obj.user.id)+"_compileroutput"
				obj.runtimeoutp="media/code/"+str(obj.user.id)+"_runtimeroutput"
				obj.processed="n"
				obj.save()
			else:
				subprocess.call(["rm","-f",obj.fil_e],shell=False)
				obj.fil_e ="media/code/"+str(request.user.id)+"_"+str(fo.cleaned_data["fil_e"].name)
				obj.processed="n"
				obj.save()
				fil = open(obj.fil_e,"w+")
				k = fo.cleaned_data["fil_e"].read()
				fil.write(k)
				fil.close()
				fil = open(obj.compileoutp,"w+")
				fil.close()
				fil = open(obj.runtimeoutp,"w+")
				fil.close()
			
			req=RequestQueue.objects.all()
			if req.exists():	
				q,created=RequestQueue.objects.get_or_create(codetocompile=obj)
							
			else : 
				q,created=RequestQueue.objects.get_or_create(codetocompile=obj)
				thread.start_new_thread(process_queue,())

			print "inserted"
			obid=obj.id
		else:
			submission_message='Improper Upload ...'
			return HttpResponseRedirect("/onlinejudge/submissionpage")
	else:
		submission_message='Improper Upload ...'
		return HttpResponseRedirect("/onlinejudge/submissionpage")
	
	return HttpResponseRedirect("/onlinejudge/submissionpage/"+str(obid))

def handle_editor(request):

	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	l=[]
	submission_message=''
	#fo = UploadFileForm(request.POST,request.FILES)
	if request.method == 'POST':
		f=open("media/code/"str(obj.user.id)+"_","w+")
		k = request.POST['code']
		f.write(k)
		obj,created = CodeToCompile.objects.get_or_create(user=request.user)
		if created is True:
			obj.compilemessage="Compiling..."
			obj.fil_e="media/code/"+str(obj.user.id)+"_"+str(fo.cleaned_data["fil_e"].name)
			obj.compileoutp="media/code/"+str(obj.user.id)+"_compileroutput"
			obj.runtimeoutp="media/code/"+str(obj.user.id)+"_runtimeroutput"
			obj.processed="n"
			obj.save()
		else:
				subprocess.call(["rm","-f",obj.fil_e],shell=False)
				obj.fil_e ="media/code/"+str(request.user.id)+"_"+str(fo.cleaned_data["fil_e"].name)
				obj.processed="n"
				obj.save()
				fil = open(obj.fil_e,"w+")
				k = fo.cleaned_data["fil_e"].read()
				fil.write(k)
				fil.close()
				fil = open(obj.compileoutp,"w+")
				fil.close()
				fil = open(obj.runtimeoutp,"w+")
				fil.close()
			
			req=RequestQueue.objects.all()
			if req.exists():	
				q,created=RequestQueue.objects.get_or_create(codetocompile=obj)
							
			else : 
				q,created=RequestQueue.objects.get_or_create(codetocompile=obj)
				thread.start_new_thread(process_queue,())
	
			print "inserted"
			obid=obj.id
		else:
			submission_message='Improper Upload ...'
			return HttpResponseRedirect("/onlinejudge/submissionpage")
	else:
		submission_message='Improper Upload ...'
		return HttpResponseRedirect("/onlinejudge/submissionpage")
	

def submissionpage(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	form = UploadFileForm();
	return render_to_response("submissionpage.html",{'form':form,'message':submission_message},context_instance=RequestContext(request))

def login(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	l=[]
	if request.method=='POST':
		print request.POST['user']
		print request.POST['pass']
		usernam=request.POST['user']
		passwor=request.POST['pass']
		user=authenticate(username=usernam, password=passwor)
		print request.user
		if user is not None:
			auth.login(request,user)
			print request.user
			toreturn = {'string':"Logged in",}
			return HttpResponseRedirect("/onlinejudge")
		else:
			toreturn = {'string':"Incorrect",}
			return render_to_response("onlinejudgehome.html", toreturn, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/onlinejudge")

def logout(request):
	if not request.user.is_anonymous():
		auth.logout(request)
	return HttpResponseRedirect("/onlinejudge")

def home(request):
	toreturn = {'string':"",}
	return render_to_response("onlinejudgehome.html",toreturn,context_instance=RequestContext(request))

def editor(request):
	return render_to_response("vim.html")
