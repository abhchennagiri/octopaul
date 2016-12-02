# This Python reads the file_count.txt and prints all the files with count > specified number


input_file = "file_count.txt"
count = int(raw_input("Enter the minimum count of the file\n"))

with open(input_file) as input:
    for line in input:
        num_lines,output_file = line.split() 
        #print num_lines,output_file
        if(int(num_lines) < count):
            print output_file
