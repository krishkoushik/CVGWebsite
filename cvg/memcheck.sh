SECONDS=0
initial=$(du -s ${2})
for ((;;))
do
	if [[ -d /proc/${1} ]] ; then
		disk_size=$(du -s ${2})
		heap_data=$(grep -s VmData* /proc/${1}/status|sed 's/[^0-9]*//g')
		stack=$(grep -s VmStk* /proc/${1}/status|sed 's/[^0-9]*//g')
		total_mem=$((stack+heap_data))
		echo $total_mem > mes.txt
		net_usage=$((disk_size-initial))
		if [ $net_usage -ge 100 ]; then
			kill -9 ${1}
			echo "Too much disk space used" > ${2}mes.txt
			break
		fi
		if [ $total_mem -ge 50000 ]; then
			kill -9 ${1}
			echo "Memory Limit Exceeded" > ${2}mes.txt
			break
		fi
		if [ $SECONDS -ge 5 ]; then
			kill -9 ${1}
			echo "Time Limit Exceeded" > ${2}mes.txt
			break
		fi
	else
		echo "Running Successful" > ${2}mes.txt
		break
	fi
done
