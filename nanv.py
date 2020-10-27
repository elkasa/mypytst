import shutil
import random
import logging
import pathlib
from zipfile import ZipFile
import os
from os.path import basename



'''
version 1.94
29/10  ANN
'''

current_dir = pathlib.Path.cwd()
logging.basicConfig(filename='logfile.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

dirpath = pathlib.Path.cwd()/'in'
dirout = pathlib.Path.cwd()/'out'
dirrejet = pathlib.Path.cwd()/'rejet'
raison = ""
assert(dirpath.is_dir())
assert(dirout.is_dir())
assert(dirrejet.is_dir())
dct = dict()
dct3 = dict()
data = dict()
data3 = dict()
header = []
footer = []

def is_valide(ae, em, bf):
    pass


def validate(ae, em, bf, res):
    pass


def reject_file(filename, raison):
    fname = filename.name
    logging.error('This file is rejected KO raison  ' + raison + fname)
    shutil.move(filename, dirrejet/fname)
    zipfile = (fname.split(".")[0])+'.zip'
    fl = pathlib.Path(dirpath/zipfile)
    if fl.is_file():
        shutil.move(fl, dirrejet/zipfile)
        logging.error('This file is rejected KO : ' + zipfile)


def post_process(filename):
    pass


def pre_process(filename):
    pass

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def newprocess(filename):
    # header = []
    # footer = []
    bf = []
    i = 0
  
    # data.clear()
    # data3.clear()
    fullstr="ANA0000"
    coef=5.2
    out_filename = dirout/filename.name
    
    with open(filename,encoding='utf-8', errors='ignore') as f:
        with open(out_filename,'w',encoding='utf-8',  errors='ignore') as out_file:
            while i < 4:
                i= i +1
                line = f.readline()
                out_file.write('%s' % line)
            #print(len(header))
            while line:
                if line[0:2] == 'AE':
                    sub=((line.split(';')[4]).split(':')[1])[0:3]
                    if sub in fullstr:
                        ael=[]
                        ae=line.split(';')
                        ae[6]="79"
                        ael.append(';'.join(ae).strip())
                        out_file.write('%s\n' % ael[0])
                        line=f.readline()
                        if line[0:2] == "EM":
                            eml=[]
                            em=line.split(';')
                            em[7]="70MD2WEW"
                            #print(em)
                            if isfloat(em[8]):
                                p=float(em[8]) - coef
                                em[10]=str(round(p,2))
                                eml.append(';'.join(em).strip())
                                out_file.write('%s\n' % eml[0])
                            else:
                                eml.append(';'.join(em).strip())
                                out_file.write('%s\n' % eml[0])
                        line=f.readline()
                        if line[0:2] == "BF":
                            bfl=[]
                            bf=line.split(';')
                            bf[5]="3570"
                            bf[6]="3640"
                            bfl.append(';'.join(bf).strip())
                            out_file.write('%s\n' % bfl[0])
                    else:
                        out_file.write('%s' % line)
                if line[0:2] == "EM":
                    out_file.write('%s' % line)
                if line[0:2] == "BF":
                    out_file.write('%s' % line)
                if line[0:2] == "DN":
                    out_file.write('%s' % line)
                    out_file.write('%s' % line)
                if line[0:2] == "SA":
                    out_file.write('%s' % line)
                if line[0:2] == "ES":
                    out_file.write('%s' % line)
                    es = line.strip()
                if line[0:2] == "EN":
                    out_file.write('%s' % line)

                line = f.readline()
            en1="EN;;A;;18;;"
            en2="EN;;A;;19;;"
            en3="EN;;A;;14;;"
            out_file.write('%s\n' % en1)
            out_file.write('%s' % en2)
            out_file.write('%s' % en3)

"""
end func process
"""
"""
output data
"""

logging.info('Start files processing  directory input : ' + dirpath.name)
logging.info('Start files processing  directory output : ' + dirout.name)
i_zip = 0
i_txt = 0
for f in dirpath.iterdir():
    if (f.name).endswith(".zip"):
        i_zip += 1
        logging.info('unzip file  : ' + f.name)
        print(f)
        shutil.unpack_archive(f, dirpath,'zip')
for f in dirpath.iterdir():
    if (f.name).endswith(".txt"):
        i_txt += 1
        logging.info('pre_process file ===>  : ' + f.name)
        # res = pre_process(f)
        newprocess(f)
        if pre_process(f) == True:
            newprocess(f)
        else:
            continue
logging.info('End processing of : ' + str(i_zip) +
             ' zip files to :' + str(i_txt) + ' txt files')
for f in dirout.iterdir():
    if (f.name).endswith(".txt"):
        logging.info('Post_process file ===>  : ' + f.name)
        post_process(f)
logging.info('End Post processing')


logging.info('End Zip ')
