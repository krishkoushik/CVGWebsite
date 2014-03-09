for i in `ldd ${1}/output | sed 's/^.*=> *//' | sed 's/ *(.*)$//'`;
do 
	cp --parents $i ${1};
done
for i in `ldd /bin/bash | sed 's/^.*=> *//' | sed 's/ *(.*)$//'`;
do 
	cp --parents $i ${1};
done
cp --parents /bin/bash ${1}
cp --parents /bin/sh ${1}
cp --parents /sbin/ldconfig ${1}
cp --parents /sbin/ldconfig.real ${1}
cp --parents /etc/ld.so.conf ${1}
cp --parents /etc/ld.so.conf.d/* ${1}
