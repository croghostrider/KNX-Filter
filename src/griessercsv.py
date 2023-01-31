#!/usr/bin/env python
"""
Read a csv file and split it into smaller files
Store the header row(s)
For every 1,000,000 rows
  Start a new file called filename-part-x.csv
  Add the header row(s)
  Add the 1,000,000 rows
  Close the new file
Usage:
  csv-splitter.py <filename> [--header_size=<lines>] [--chunk_size=<lines>]
"""
import os.path
import os
import glob


def split_file(filename, header_size, chunk_size):
    print(f"Processing {filename} with header of {header_size} lines into chunks of {chunk_size}")
    split_fname = os.path.basename(filename).rpartition('.')
    outfile_extension = split_fname[-1]
    outfile_stub = split_fname[-3]
    if not os.path.exists('outputs'):
        os.mkdir('outputs')


    num_rows = sum(1 for _ in open(filename, "r", encoding='windows-1252'))

    if num_rows > 65500:

        outfile_number = 1
        with open(filename, "r", encoding='windows-1252') as big_file:
            header = [big_file.readline() for _ in range(header_size)]
            line = "SEED"
            while line:
                outfile_name = f"outputs/{outfile_stub}-{outfile_number}.{outfile_extension}"
                outfile_number += 1
                print(f"Outputting to file: {outfile_name}")
                with open(outfile_name, "w") as outfile:
                    outfile.writelines(header)
                    for _ in range(chunk_size):
                        line = big_file.readline()
                        outfile.writelines(line)
        
        os.remove(filename)


def get_xmls(files):
    xml_files = glob.glob(files +"/*.csv")
    for xml_file in xml_files:
        split_file(xml_file, 0, 65500)


get_xmls('C:/Users/Vinko/Desktop/test')
