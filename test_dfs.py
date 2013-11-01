#!/usr/bin/env/python
# -*- coding: utf-8 -*-

CSV_CATALOG = '.\\results\\'
SERVERS = 2

import os
import csv
from random import shuffle
from subprocess import Popen, PIPE, STDOUT

def runtest_write():
    import time
    CSV_FILE_PATH_WRITE = CSV_CATALOG + "dfs_%d_servers_write.csv" % SERVERS
    text_files = [f for f in os.listdir(".\\initial") if f.endswith('.txt')]
    time_operations = []
    # запись данных в DFS
    shuffle(text_files)
    for file_name in text_files:
        file_path = str(".\\initial\\"+file_name)
        f = open(file_path, 'r')
        message = '[W]['+file_name+']'+f.read()
        f.close()
        start_time=time.time()
        p = Popen(["python", "client.py", '127.0.0.1', '5000' , message], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.communicate()[0]
        finish_time=time.time()
        ready_time = float("%.10f" % (finish_time-start_time))
        time_operations.append(ready_time)
    
    with open(CSV_FILE_PATH_WRITE, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for time in time_operations:
            csv_writer.writerow([str(time).replace('.',',')])

def runtest_read():
        import time
        CSV_FILE_PATH_READ = CSV_CATALOG + "dfs_%d_servers_read.csv" % SERVERS
        text_files = [f for f in os.listdir(".\\initial") if f.endswith('.txt')]
        time_operations = []
        # чтение данных из DFS
        shuffle(text_files)
        for file_name in text_files:
            message = '[R]['+file_name+']'
            start_time_read=time.time()
            p = Popen(["python", "client.py", '127.0.0.1', '5000' , message], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            p.communicate()[0]
            finish_time_read=time.time()
            ready_time_read = float("%.10f" % (finish_time_read-start_time_read))
            time_operations.append(ready_time_read)
        
        with open(CSV_FILE_PATH_READ, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)
            for time in time_operations:
                csv_writer.writerow([str(time).replace('.',',')])

if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        sys.exit("Using test_dfs.py [SERVERS]")
    SERVERS = int(sys.argv[1])
    runtest_write()
    runtest_read()