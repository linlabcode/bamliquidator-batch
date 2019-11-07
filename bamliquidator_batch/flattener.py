#!/usr/bin/env python

import argparse
import csv
import os
import tables

def write_tab(table, file_names, output_directory, log=False):
    chromosome_to_file_writer_pair = {}

    columns = [col for col in table.colnames if col != "chromosome"]
    columns = [col if col != "file_key" else "file_name" for col in columns]

    for row in table:
        chromosome = row["chromosome"]
        if chromosome not in chromosome_to_file_writer_pair:
            tab_file_path = os.path.join(output_directory, table.name + "_" + chromosome + ".tab")
            if log:
                print("Writing", tab_file_path)

            tab_file = open(tab_file_path, 'wb')
            writer = csv.writer(tab_file, delimiter='\t')
            writer.writerow(columns)
            chromosome_to_file_writer_pair[chromosome] = (tab_file, writer)
        else:
            _, writer = chromosome_to_file_writer_pair[chromosome]

        # pickup here: translate file_key to file_name
        row_list = []
        for col in columns:
            if col == "file_name":
                row_list.append(file_names[row["file_key"]])
            else:
                row_list.append(row[col])
            
        writer.writerow(row_list)

    for tab_file, _ in list(chromosome_to_file_writer_pair.values()):
        tab_file.close()

def write_tab_for_all(h5_file, output_directory, log=False):
    for table in h5_file.root:
        if table.name not in ("files", "file_names"):
            write_tab(table, h5_file.root.file_names, output_directory, log)

def main():
    parser = argparse.ArgumentParser(description='Writes bamliquidator_batch.py hdf5 tables into tab delimited '
        'text files, one for each chromosome.  Note that this is provided as a convenience, but it is hoped that '
        'the hdf5 files will be used directly since they are much more efficient to work with -- e.g. please see '
        'http://www.pytables.org/ for easy to use Python APIs and '
        'http://www.hdfgroup.org/products/java/hdf-java-html/hdfview/ for an easy to use GUI for browsing HDF5 '
        'files.  For more info, please see https://github.com/BradnerLab/pipeline/wiki/bamliquidator .')
    parser.add_argument('-t', '--table', default=None, help='the table to write to hdf5, e.g. "region_counts" for '
        'a regions counts.h5 file, or one of the following for a uniform bins counts.h5 file: "bin_counts", '
        '"normalized_counts", "sorted_summary", or "summary".  If none specified flattens every table in the h5 file, '
        'using the table name as a file prefix.')
    parser.add_argument('h5_file', help='the hdf5 file generated by bamliquidator_batch.py')
    parser.add_argument('output_directory', help='directory to store the tab files (must already exist)')
    args = parser.parse_args()

    h5_file = tables.open_file(args.h5_file, mode = "r")

    log = True

    if args.table:
        table = h5_file.get_node("/" + args.table)
        write_tab(table, h5_file.root.file_names, args.output_directory, log)
    else:
        write_tab_for_all(h5_file, args.output_directory, log)
    
    h5_file.close()

if __name__ == "__main__":
    main()

'''
   The MIT License (MIT) 

   Copyright (c) 2013 John DiMatteo (jdimatteo@gmail.com) 

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE. 
'''