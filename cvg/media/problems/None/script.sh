count=0;
for((i=0;i<4;i++)); do
python sandcodenew.py ${1} ${2} ${3} ${4} "${!}${i}.jpg"
outputfile="${1}stdout"
sed -i '/^[[:space:]]*$/d;s/[[:space:]]*$//' ${outputfile}
while read -r a && read -r b <&3; do
if [ "${a}" == "${b}" ]
then
count=$((count+1))
fi
done < "${1}${i}" 3<${outputfile}
echo $count
done
count=$((count/10))
echo $count > score
