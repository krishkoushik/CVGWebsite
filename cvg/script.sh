NUM_TEST_CASES=4
count=0;
for((i=0;i<${NUM_TEST_CASES};i++)); do
python sandcodenew.py ${1} ${2} ${3} ${4} "${1}${i}.jpg"
echo "$1 $2 $3 $4 "> hello
outputfile="${1}stdout"
sed -i '/^[[:space:]]*$/d;s/[[:space:]]*$//' ${outputfile}
while read -r a && read -r b <&3; do
if [ "${a}" == "${b}" ]
then
count=$((count+1))
echo $count > "$count"
fi
done < "${1}${i}" 3<${outputfile}
echo $count
done
count=$((count/NUM_TEST_CASES))
echo $count > "${1}score"
