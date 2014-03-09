from sandbox import *
import subprocess, shlex
import sys
from ctypes import Structure, sizeof
from ctypes import c_uint32, c_uint64, c_int32, c_int64, c_int
from platform import system, machine
from sandbox import *

# check platform type
if system() not in ('Linux', ) or machine() not in ('x86_64', 'i686', ):
	raise AssertionError("Unsupported platform type.\n")



class Policy(SandboxPolicy,Sandbox):

	def __init__(self, *args, **kwds):
		# Linux system calls for fd write
		if machine() == 'x86_64': # x86_64 (multiarch) system calls
			x86_64, i686 = 0, 1
			SC_write = ((1, x86_64), (4, i686), )
			SC_pwrite64 = ((18, x86_64), (181, i686), )
			SC_writev = ((20, x86_64), (146, i686), )
			SC_pwritev = ((296, x86_64), (334, i686), )
		else: # i686 system calls
			SC_write = (4, )
			SC_pwrite64 = (181, )
			SC_writev = (146, )
			SC_pwritev = (334, )
		# table of system call rules
		self.sc_table = {}
		for entry, handler in zip((SC_write, SC_pwrite64, SC_writev, SC_pwritev), \
			(self.SYS_write, self.SYS_write, self.SYS_writev, self.SYS_writev)):
			for sc in entry:
			    self.sc_table[sc] = handler
		# policy internal states
		self.written_bytes = 0
		self.pending_bytes = 0
		# initalize as a polymorphic sandbox-and-policy object
		SandboxPolicy.__init__(self)
		Sandbox.__init__(self, *args, **kwds)
		self.policy = self
		pass
	def probe(self):
		# add custom entries into the probe dict
		d = Sandbox.probe(self, False)
		d['out'] = (self.written_bytes, self.written_bytes + self.pending_bytes)
		return d
	def SYS_write(self, e, a): # write / pwrite64
		abi64 = (machine() == 'x86_64' and e.ext0 == 0)
		ssize_t, size_t = (c_int64, c_uint64) if abi64 else (c_int32, c_uint32)
		if e.type == S_EVENT_SYSCALL:
			self.pending_bytes = size_t(e.ext3).value
		else:
			if ssize_t(e.ext1).value > 0:
			    self.written_bytes += ssize_t(e.ext1).value
			self.pending_bytes = 0
		return self._output_check(e, a)
	def SYS_writev(self, e, a): # writev / pwritev
		abi64 = (machine() == 'x86_64' and e.ext0 == 0)
		ssize_t = c_int64 if abi64 else c_int32
		if e.type == S_EVENT_SYSCALL:
			# enumerate the struct iovec[] to count pending bytes
			address, iovcnt = e.ext2, c_int(e.ext3).value
			self.pending_bytes = 0
			for i in range(iovcnt):
				iovec = self._dump_iovec(abi64, address)
				self.pending_bytes += iovec.iov_len
				address += sizeof(iovec)
		else:
			if ssize_t(e.ext1).value > 0:
				self.written_bytes += ssize_t(e.ext1).value
			self.pending_bytes = 0
		return self._output_check(e, a)
	def _dump_iovec(self, abi64, address):
		# dump a struct iovec object from the given address
		typeid = T_ULONG if abi64 else T_UINT
		size_t, char_p = (c_uint64, ) * 2 if abi64 else (c_uint32, ) * 2
		class struct_iovec(Structure): # from manpage writev(2)
			 _fields_ = [('iov_base', char_p), ('iov_len', size_t), ]
		return struct_iovec(self.dump(typeid, address), \
			self.dump(typeid, address + sizeof(char_p)))
	def _output_check(self, e, a):
		# compare current written + pending bytes against the quota
		if self.written_bytes + self.pending_bytes > self.quota[3]:
			return self._KILL_OL(e, a)
		return self._CONT(e, a)
	def _CONT(self, e, a): # continue
		a.type = S_ACTION_CONT
		return a


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



