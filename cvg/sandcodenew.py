from sandbox import *
import subprocess, shlex
import sys
from ctypes import Structure, sizeof
from ctypes import c_uint32, c_uint64, c_int32, c_int64, c_int
from platform import system, machine

# check platform type
if system() not in ('Linux', ) or machine() not in ('x86_64', 'i686', ):
	raise AssertionError("Unsupported platform type.\n")
	
class Policy(SandboxPolicy,Sandbox):
	def __init__(self, *args, **kwds):
		# Linux system calls for fd write and memory declaration
		if machine() == 'x86_64': # x86_64 (multiarch) system calls
			x86_64, i686 = 0, 1
			SC_write = ((1, x86_64), (4, i686), )
			SC_pwrite64 = ((18, x86_64), (181, i686), )
			SC_writev = ((20, x86_64), (146, i686), )
			SC_pwritev = ((296, x86_64), (334, i686), )
			SC_brk = ((12, x86_64), (45, i686), )
			SC_mmap = ((9, x86_64), (90, i686), )
			SC_mmap2 = ((192, i686), )
			SC_mremap = ((25, x86_64), (163, i686), )
		else: # i686 system calls
			SC_write = (4, )
			SC_pwrite64 = (181, )
			SC_writev = (146, )
			SC_pwritev = (334, )
			SC_brk = (45, )
			SC_mmap = (90, )
			SC_mmap2 = (192, )
			SC_mremap = (163, )
		# table of system call rules
		self.sc_table = {}
		for entry, handler in zip((SC_write, SC_pwrite64, SC_writev, SC_pwritev), \
			(self.SYS_write, self.SYS_write, self.SYS_writev, self.SYS_writev)):
			for sc in entry:
				self.sc_table[sc] = handler			    
		for entry, handler in zip((SC_brk, SC_mmap, SC_mmap2, SC_mremap), \
            (self.SYS_brk, self.SYS_mmap, self.SYS_mmap, self.SYS_mremap)):
			for sc in entry:
				self.sc_table[sc] = handler
		# policy internal states
		self.written_bytes = 0
		self.pending_bytes = 0
		self.data_seg_end = 0 # data segment end address
		self.pending_alloc = 0 # pending memory allocation (kB)
		# initalize as a polymorphic sandbox-and-policy object
		SandboxPolicy.__init__(self)
		Sandbox.__init__(self, *args, **kwds)
		#print self.quota
		self.policy = self
		pass
		
	def __call__(self, e, a):
		#print "mememe"
		#vm_peak = max(self.probe()['mem'])
		#print "hohohh"
		#print vm_peak
		#print self.quota[2]
		#if vm_peak > self.quota[2]:
		#	return self._KILL_ML(e, a)
	# handle SYSCALL/SYSRET events with local rules
		if e.type in (S_EVENT_SYSCALL, S_EVENT_SYSRET):
			sc = (e.data, e.ext0) if machine() == 'x86_64' else e.data
			if sc in self.sc_table:
				return self.sc_table[sc](e, a)
	   # bypass other events to base class
		return SandboxPolicy.__call__(self, e, a)
		
	#System Calls Handling	
		
	def SYS_brk(self, e, a):
		#print "gen"
		if e.type == S_EVENT_SYSCALL:
			# pending data segment increment
			if e.ext1 > 0:
				incr = e.ext1 - self.data_seg_end
				#print "oho"
				return self._memory_check(e, a, incr)
		else:
			# update data segment end address
			self.data_seg_end = e.ext1
		#print "aha"
		return self._memory_check(e, a)
		
	def SYS_mmap(self, e, a):
		#print "gil"
		MAP_PRIVATE = 0x02 # from <bits/mman.h>
		if e.type == S_EVENT_SYSCALL:
			size, flags, fd = e.ext2, c_int(e.ext4).value, c_int(e.ext5).value
			# forbid non-pivate mapping or mapping to unknown file descriptors
	#		if flags & MAP_PRIVATE == 0 or fd not in (-1, 0, 1, 2):  #Should this really be commented?
	#			return self._KILL_RF(e, a)
			# pending memory mapping
			return self._memory_check(e, a, size)
		return self._memory_check(e, a)
		
	def SYS_mremap(self, e, a):
		# fallback to lazy (non-predictive) quota limitation
		#print "chefk"
		return self._memory_check(e, a)
		
	def _memory_check(self, e, a, incr=0):
		# compare current mem usage (incl. pending alloc) against the quota
		self.pending_alloc = incr / 1024
		#print "checking"
		#print max(self.probe()['mem'])
		#print "!!"
		if max(self.probe()['mem']) * 1024 > self.quota[2]:
			#print "inga"
			return self._KILL_ML(e, a)
		#print "inga"
		return self._CONT(e, a)

	def SYS_write(self, e, a): # write / pwrite64
		abi64 = (machine() == 'x86_64' and e.ext0 == 0)
		ssize_t, size_t = (c_int64, c_uint64) if abi64 else (c_int32, c_uint32)
		#print "hillo"
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
		#print "hollo"
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
		#print "gkl"
		class struct_iovec(Structure): # from manpage writev(2)
			 _fields_ = [('iov_base', char_p), ('iov_len', size_t), ]
		return struct_iovec(self.dump(typeid, address), \
			self.dump(typeid, address + sizeof(char_p)))

#Utility Functions
			
	def _output_check(self, e, a):
		# compare current written + pending bytes against the quota
		#print "kkl"
		#print str(self.written_bytes)+" written"
		if self.written_bytes + self.pending_bytes > self.quota[3]:
			return self._KILL_OL(e, a)
		return self._CONT(e, a)

	def probe(self):
		# add custom entries into the probe dict
		d = Sandbox.probe(self, False)
		d['mem'] = (d['mem_info'][1], d['mem_info'][0] + self.pending_alloc)
		return d
		

#Function for Killing/Continuing processes


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
		
		
		
if __name__ == '__main__':
	subprocess.call(shlex.split("chroot "+sys.argv[1]+" sbin/ldconfig"),stderr=open("error","w"),shell=False)
	#print "hoho"
	f = open(sys.argv[1]+"mes.txt","w")
	f.write("Running Successful")
	f.close()
	s = Policy(["./"+sys.argv[1]+"output"]+sys.argv[5:],jail="./"+sys.argv[1],quota=dict(cpu=int(sys.argv[2]),disk=int(sys.argv[3]),memory=int(sys.argv[4]),wallclock=15000),stderr=open(sys.argv[1]+"error.txt","w"),stdout = open(str(sys.argv[1]+"stdout"),"w"))
	s.run()
	#print s.quota[0]
	print "Result : "+str(s.result)
	if s.result==S_RESULT_OK:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Running Successful")
		f.close()
	elif s.result==S_RESULT_RF:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Restricted Function Access")
		f.close()
	elif s.result==S_RESULT_TL:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Time Limit Exceeded")
		f.close()
	elif s.result==S_RESULT_OL:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Disk Space Exceeded")
		f.close()
	elif s.result==S_RESULT_ML:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Segmentation Fault")
		f.close()
	elif s.result==S_RESULT_AT:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Bad Exit Code")
		f.close()
	else:
		f = open(sys.argv[1]+"mes.txt","w")
		f.write("Not Run Properly "+str(s.result))
		f.close()
	a = s.probe('mem')
	if s.result!=S_RESULT_OK:
		fil = open(sys.argv[1]+"stdout","w");
		fil.close()


