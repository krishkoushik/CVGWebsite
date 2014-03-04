from django.shortcuts import HttpResponse,render_to_response, RequestContext, HttpResponseRedirect
import re
from django.contrib.auth import authenticate
from django.contrib import auth
from onlinejudge.models import UploadFileForm, CodeToCompile, Problem, Contest
from onlinejudge.models import RequestQueue, CurrentContest
import os
import subprocess,shlex
from django.core.files import File
import thread
from django.shortcuts import get_object_or_404
from django.db.models import Q

def contest(request,contest_id):
	cont = get_object_or_404(Contest,id=contest_id)
	return render_to_response("ContestProblems.html",{'problems':Problem.objects.filter(contest=cont),'cont':cont,},context_instance=RequestContext(request))

def challenges(request,contest_id):
#Add login if the user needs to be logged in for viewing the challenges
	cont = get_object_or_404(Contest,id=contest_id)
	return render_to_response("challenges.html",{'problems':Problem.objects.filter(contest=cont),'cont':cont,},context_instance=RequestContext(request))

def practice(request):
#Add login if the user needs to be logged in for viewing the challenges
	contests = Contest.objects.filter(~Q(id=CurrentContest.objects.get(id=1).contest.id))
	return render_to_response("practice.html",{'contests':contests,},context_instance=RequestContext(request))

def process_queue():
	
	while True:
		req=RequestQueue.objects.all()
		if req.exists():
			for qr in req:
				handle_uploaded_file(qr.codetocompile.id)
				qr.delete()
		else:
			break


def handle_uploaded_file(obid):
		
#Compiling code and storing the compile message in object
	code = get_object_or_404(CodeToCompile,id=obid)
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
		out2=subprocess.Popen(['bash','memcheck.sh',str(out1.pid)],shell=False);
		stdo,stder = out1.communicate()
		stdo,stder = out2.communicate()
		runt.close()
	else :
		code.compilemessage = "Compile Failed"
	
	#writing runtime message (error) to file pointed by object
	fil = File(open("runtimemessage.txt","r"))
	fi = open(code.runtimeoutp,"w")
	fi.write(fil.read())
	fil.close()
	fi.close()

	fil = File(open("mes.txt","r"))
	code.runtimemessage = fil.readline()
	fi.close()

	code.processed='y'
	code.save()

	#deleting the temporarily created files
	subprocess.call(["rm","-f","compilemessage.txt","runtimemessage.txt","mes.txt","output"],shell=False)

	
	#To be transferred to another function

def viewsubmission(request,obid):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	
	code=get_object_or_404(CodeToCompile,id=obid)
	if code.user!=request.user:
		return HttpResponseRedirect("/onlinejudge")

	if code.processed=='y':
		a = open(code.fil_e,"r")
		b = open(code.compileoutp,"r")
		c = open(code.runtimeoutp,"r")
		return render_to_response('submitted.html', {'fil_e':a,'compile':b,'runtime':c,'code':code},context_instance=RequestContext(request))
	else : 
		return render_to_response('runn.html',{'obid':obid},context_instance=RequestContext(request))

submission_message=''
def upload_file(request,problem_id):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	l=[]
	submission_message=''
	fo = UploadFileForm(request.POST,request.FILES)
	if request.method == 'POST':
		if fo.is_valid():
			form = request.FILES
#Problem object with problem id will be ensured during problem creation
			prob = get_object_or_404(Problem,id=problem_id)
			obj,created = CodeToCompile.objects.get_or_create(user=request.user,problemid=prob)
			if created is True:
				obj.compilemessage="Compiling..."
				obj.runtimemessage="Not Run..."

#Creating a file with the uploaded name
				obj.fil_e="media/code/"+str(obj.user.id)+"_"+str(problem_id)+"_"+str(fo.cleaned_data["fil_e"].name)
				fil = open(obj.fil_e,"w+")
				k = fo.cleaned_data["fil_e"].read()
				fil.write(k)
				fil.close()

#Creating files for compile and runtime output
				obj.compileoutp="media/code/"+str(obj.user.id)+"_"+str(problem_id)+"_compileroutput"
				obj.runtimeoutp="media/code/"+str(obj.user.id)+"_"+str(problem_id)+"_runtimeroutput"

#Relating to the problem
				obj.status="In the queue" #This should be changed to Processing when it is processed
				obj.processed="n"
				obj.save()

			else:

#Deleting the previous file for this object and saving the new uploaded file
				subprocess.call(["rm","-f",obj.fil_e],shell=False)
				obj.fil_e ="media/code/"+str(request.user.id)+"_"+str(problem_id)+"_"+str(fo.cleaned_data["fil_e"].name)
				obj.compilemessage="Compiling..."
				obj.runtimemessage="Not Run..."
				obj.processed="n"
				obj.status="In the queue" #This should be changed to Processing when it is processed
				obj.save()
				fil = open(obj.fil_e,"w+")
				k = fo.cleaned_data["fil_e"].read()
				fil.write(k)
				fil.close()

#saving the new compile and runtime files
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

			obid=obj.id
		else:
			submission_message='Improper Upload ...'
			return HttpResponseRedirect("/onlinejudge/submissionpage/"+str(problem_id))
	else:
		submission_message='Improper Upload ...'
		return HttpResponseRedirect("/onlinejudge/submissionpage/"+str(problem_id))
	
	return HttpResponseRedirect("/onlinejudge/viewsubmission/"+str(obid))

def submissionpage(request,problem_id):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	prob = get_object_or_404(Problem,id=problem_id)
	form = UploadFileForm();
	return render_to_response("submissionpage.html",{'form':form,'message':submission_message,'problem_id':prob.id,},context_instance=RequestContext(request))

def login(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	l=[]
	if request.method=='POST':
		usernam=request.POST['user']
		passwor=request.POST['pass']
		user=authenticate(username=usernam, password=passwor)
		if user is not None:
			auth.login(request,user)
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
	toreturn = {'string':"",'curr_contest':CurrentContest.objects.get(id=1).contest.id}
	return render_to_response("onlinejudgehome.html",toreturn,context_instance=RequestContext(request))

