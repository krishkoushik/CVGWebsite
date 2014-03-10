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
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	cont = get_object_or_404(Contest,id=contest_id)
	return render_to_response("ContestProblems.html",{'problems':Problem.objects.filter(contest=cont),'cont':cont,},context_instance=RequestContext(request))

def challenges(request,contest_id):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	cont = get_object_or_404(Contest,id=contest_id)
	return render_to_response("challenges.html",{'problems':Problem.objects.filter(contest=cont),'cont':cont,},context_instance=RequestContext(request))

def practice(request):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	l=[]
	for con in Contest.objects.all():
		if con.id!=1 :
			l.append(con);
	contests = l
	return render_to_response("practice.html",{'contests':contests,},context_instance=RequestContext(request))

def process_queue():
	
	print "queue"
	while True:
		req=RequestQueue.objects.all()
		if req.exists():
			for qr in req:
				handle_uploaded_file(qr.codetocompile.id)
				qr.delete()
		else:
			break

def handle_uploaded_file(obid):
	
	print "youoiu"	
#Compiling code and storing the compile message in object
	code = get_object_or_404(CodeToCompile,id=obid)
	prob = code.problemid
	dir_jail_name = "media/code/"+str(code.user.id)+"_"+str(code.problemid.id)+"/"	
	arg=shlex.split("g++ -I/usr/local/include/opencv -I/usr/local/include "+code.fil_e+" /usr/local/lib/libopencv_calib3d.so /usr/local/lib/libopencv_contrib.so /usr/local/lib/libopencv_core.so /usr/local/lib/libopencv_features2d.so /usr/local/lib/libopencv_flann.so /usr/local/lib/libopencv_gpu.so /usr/local/lib/libopencv_highgui.so /usr/local/lib/libopencv_imgproc.so /usr/local/lib/libopencv_legacy.so /usr/local/lib/libopencv_ml.so /usr/local/lib/libopencv_nonfree.so /usr/local/lib/libopencv_objdetect.so /usr/local/lib/libopencv_photo.so /usr/local/lib/libopencv_stitching.so /usr/local/lib/libopencv_superres.so /usr/local/lib/libopencv_ts.so /usr/local/lib/libopencv_video.so /usr/local/lib/libopencv_videostab.so -o "+dir_jail_name+"output")
	comp = open(dir_jail_name+"compilemessage.txt","wb+")#creating a compile message file
	out=subprocess.call(arg,stderr=comp,shell=False)
	comp.close()
	print dir_jail_name
#return 
	
	#writing the compile file
	fil = open(dir_jail_name+"compilemessage.txt","r")
	fi = open(str(code.compileoutp),"w")
	fi.write(fil.read())
	fil.close()
	fi.close()
	
	print dir_jail_name+"hi"
	#Creating the jail environment
	subprocess.call(["bash","makejail.sh",dir_jail_name,],shell=False)

	#Running code and storing runtime message
	
	runt = open(dir_jail_name+"runtimemessage.txt","wb+")#creating a runtimemessage file
	runt.close()
	runt = open(dir_jail_name+"mes.txt","wb+")#creating a memcheck message file
	runt.close()
	if out==0 :
		code.compilemessage = 'Successfully Compiled'
		arg=shlex.split("sudo python sandcodenew.py "+dir_jail_name+" "+prob.time_limit+" "+prob.disk_limit+" "+prob.mem_limit+" "+prob.arguements)
		runt = open(dir_jail_name+"runtimemessage.txt","wb+")
		out1=subprocess.Popen(arg,stdout=runt,shell=False)
#out2=subprocess.Popen(['bash','memcheck.sh',str(out1.pid),dir_jail_name,],shell=False);
		stdo,stder = out1.communicate()
#		stdo,stder = out2.communicate()
		runt.close()
	else :
		code.compilemessage = "Compile Failed"
	
	#writing runtime message (error) to file pointed by object
	fil = File(open(dir_jail_name+"runtimemessage.txt","r"))
	fi = open(code.runtimeoutp,"w")
	fi.write(fil.read())
	fil.close()
	fi.close()

	fil = File(open(dir_jail_name+"mes.txt","r"))
	code.runtimemessage = fil.readline()
	fi.close()

	code.processed='y'
	code.save()

	#deleting the temporarily created files
#subprocess.call(["rm","-f","compilemessage.txt","runtimemessage.txt","mes.txt","output"],shell=False)

	
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
			#Creating Jail directory

			dir_jail_name = "media/code/"+str(obj.user.id)+"_"+str(problem_id)+"/"
			subprocess.call(["rm","-rf",dir_jail_name],shell=False)
			subprocess.call(["mkdir","-p",dir_jail_name])

			if created is True:
				obj.compilemessage="Compiling..."
				obj.runtimemessage="Not Run..."

#Creating a file with the uploaded name
				obj.fil_e=dir_jail_name+str(obj.user.id)+"_"+str(problem_id)+"_"+str(fo.cleaned_data["fil_e"].name)
				fil = open(obj.fil_e,"w+")
				k = fo.cleaned_data["fil_e"].read()
				fil.write(k)
				fil.close()

#Creating files for compile and runtime output
				obj.compileoutp=dir_jail_name+str(obj.user.id)+"_"+str(problem_id)+"_compileroutput"
				obj.runtimeoutp=dir_jail_name+str(obj.user.id)+"_"+str(problem_id)+"_runtimeroutput"

#Relating to the problem
				obj.status="In the queue" #This should be changed to Processing when it is processed
				obj.processed="n"
				obj.save()	


			else:

#Deleting the previous file for this object and saving the new uploaded file
				subprocess.call(["rm","-f",obj.fil_e],shell=False)
				obj.fil_e =dir_jail_name+str(request.user.id)+"_"+str(problem_id)+"_"+str(fo.cleaned_data["fil_e"].name)
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

def handle_editor(request,problem_id):

	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge");
	l=[]
	submission_message=''
	#fo = UploadFileForm(request.POST,request.FILES)
	if request.method == 'POST':
		prob = get_object_or_404(Problem,id=problem_id)
		obj,created = CodeToCompile.objects.get_or_create(user=request.user,problemid=prob)
		#Creating the jail directory
		dir_jail_name = "media/code/"+str(obj.user.id)+"_"+str(problem_id)+"/"
		subprocess.call(["rm","-rf",dir_jail_name],shell=False)
		subprocess.call(["mkdir","-p",dir_jail_name])
		if created is True:
			
			f=open(dir_jail_name+str(request.user.id)+"_"+str(problem_id)+"_"+"editor_file.cpp","w+")
			k = request.POST['code']
			f.write(k)
                        obj.compilemessage="Compiling..."
			obj.fil_e=dir_jail_name+str(obj.user.id)+"_"+str(problem_id)+"_"+"editor_file.cpp"			
			obj.compileoutp=dir_jail_name+str(obj.user.id)+"_compileroutput"
			obj.runtimeoutp=dir_jail_name+str(obj.user.id)+"_runtimeroutput"
			obj.processed="n"
			obj.save()
		else:
			subprocess.call(["rm","-f",obj.fil_e],shell=False)
			
			f=open(dir_jail_name+str(request.user.id)+"_"+str(problem_id)+"_"+"editor_file.cpp","w+")
			k = request.POST['code']
			f.write(k)
			obj.fil_e =dir_jail_name+str(obj.user.id)+"_"+str(problem_id)+"_"+"editor_file.cpp"	
			obj.processed="n"
			obj.save()
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
	for con in CurrentContest.objects.all():
		if con.id==1 :	
			toretur = {'string':"",'curr_contest':con.contest.id}#to be extended for more contests
			return render_to_response("onlinejudgehome.html",toretur,context_instance=RequestContext(request))
	toretur = {'string':"No Current Contests",'curr_contest':1}
	return render_to_response("onlinejudgehome.html",toretur,context_instance=RequestContext(request))

def editor(request,problem_id):
	if request.user.is_anonymous():
		return HttpResponseRedirect("/onlinejudge")
	return render_to_response("vim.html",{'problem_id':problem_id},context_instance=RequestContext(request))
