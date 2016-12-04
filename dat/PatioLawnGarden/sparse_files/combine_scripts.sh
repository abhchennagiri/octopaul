wc -l * | head -n 1000 > file_count.txt

python ../../remove_sparse_file.py file_count.txt > sparse_files.txt

mkdir sparse_files

sh ../../mv_sparse_files.sh
