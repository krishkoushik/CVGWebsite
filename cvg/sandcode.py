from sandbox import *
import subprocess, shlex
import sys
from ctypes import Structure, sizeof
from ctypes import c_uint32, c_uint64, c_int32, c_int64, c_int
from platform import system, machine
from sandbox import *



class Policy(SandboxPolicy,Sandbox):
	def _KILL_RF(self, e, a):
		a.type, a.data = S_ACTION_KILL, S_RESULT_RF
		return a
	def _KILL_TL(self, e, a):
		a.type, a.data = S_ACTION_KILL, S_RESULT_TL
		return a
	def _KILL_OL(self, e, a):
		a.type, a.data = S_ACTION_KILL, S_RESULT_OL
		return a
	def _KILL_ML(self, e, a):
		a.type, a.data = S_ACTION_KILL, S_RESULT_ML
		return a

subprocess.call(shlex.split("chroot "+sys.argv[1]+" sbin/ldconfig"),stderr=open("error","w"),shell=False)
print "hoho"
f = open(sys.argv[1]+"mes.txt","w")
f.write("Running Successful")
f.close()
s = Policy(["./"+sys.argv[1]+"output"]+sys.argv[2:],jail="./"+sys.argv[1],quota=dict(cpu=2000,disk=100,mem=100,wallclock=3000))
s.run()
print s.result
if s.result==S_RESULT_RF:
	f = open(sys.argv[1]+"mes.txt","w")
	f.write("Restricted Function Access")
	f.close()
if s.result==S_RESULT_TL:
	f = open(sys.argv[1]+"mes.txt","w")
	f.write("Time Limit Exceeded")
	f.close()
if s.result==S_RESULT_OL:
	f = open(sys.argv[1]+"mes.txt","w")
	f.write("Disk Space Exceeded")
	f.close()
if s.result==S_RESULT_ML:
	f = open(sys.argv[1]+"mes.txt","w")
	f.write("Memory Limit Exceeded")
	f.close()
print s.probe()



