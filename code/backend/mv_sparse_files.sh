# Bash Script to move the sparse into a different directory

file_name="sparse_files.txt"

num_lines=`wc -l "sparse_files.txt" | awk -F" " '{print $1}'`
START=1
## save $START, just in case if we need it later ##
i=$START
echo $num_lines
#mkdir ./sparse_files
cat $file_name | while read line
do
mv $line ./sparse_files
done  
