import shutil
import random
import logging
import pathlib
from zipfile import ZipFile
import os
from os.path import basename



'''
version 1.0
29/10  ANN
'''

current_dir = pathlib.Path.cwd()
logging.basicConfig(filename='logfile.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

dirin = pathlib.Path.cwd()/'in'
dirout = pathlib.Path.cwd()/'out'
dirrejet = pathlib.Path.cwd()/'rejet'
raison = ""
assert(dirin.is_dir())
assert(dirout.is_dir())
assert(dirrejet.is_dir())

header = []
body   = []
footer = []
action_filename = dirin/'actionfile.lst'

ae_template="AE;;A;;;1301825;79;0.8;;D;AZI;;HMA;NGF;;;;15;504;;"
em_template="EM;;A;;<BYTEL: >;117;; 70M02W;40.5;I;45.95;;;;Tcode;0;"
bf_template="BF;;A;;; 3570;3640;M;MXA;"

em=em_template.split(';')
bf=bf_template.split(';')

    

logging.info('Start files processing  directory input : ' + dirin.name)
logging.info('Start files processing  directory output : ' + dirout.name)

def getTcode(filename):
    filename = dirin/filename
    if filename.is_file():
        with open(filename,encoding='utf-8', errors='ignore') as ff:
            line= ff.readline()
            tmp=line.split()
            s=str(tmp[-1]).strip(')')
            return s
def print_out(filename,ae):
    filename = dirin/filename
    out_filename= dirout/filename.name
    if filename.is_file():
        with open(filename,encoding='utf-8', errors='ignore') as f:
            #print(filename)
            lines= f.readlines()
            res=[]
            res=lines[:4] + ae
            with open(out_filename, 'w') as out_file:
                for i in range(0, 3):
                    out_file.write('%s' % res[i])
                for i in range(4, len(res)):
                    out_file.write('%s\n' % res[i])
                for i in range(4, len(lines)):
                    #print(lines[i])
                    out_file.write('%s' % lines[i])


        
with open(action_filename,encoding='utf-8', errors='ignore') as f:
    lines=f.readlines()
    for i, line in enumerate(lines[2:]):
            #:q
            #print(line)
            data=line.split(":")
            filename=data[0]
            Tcode=getTcode(filename)
            #print(Tcode)
            ae=[]
            for  j,d in enumerate(data[1:]):
                A=d.split(";")
                ael=ae_template.split(';')
                ael[9]=A[0]
                ael[11]=A[1]
                ael[12]=str(A[2])
                ae.append(';'.join(ael))
                ae.append(';'.join(em))
                ae.append(';'.join(bf))
            #print(ae)
            print_out(data[0],ae)        
        

logging.info('End Post processing')
