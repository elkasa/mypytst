import shutil
import random
import logging
import pathlib
from zipfile import ZipFile
import os
from os.path import basename


'''
version 1.6
27/08  restore en
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


def is_valide(ae, em, bf):
    if ae == "":
        return False
    elif em == "":
        return False
    elif ae.split(";")[3] == "":
        return False
    elif float(em.split(";")[8]) < 30:
        return False
    else:
        return True


def validate(ae, em, bf, res):
    res = []
    res3 = []
    f0 = '1900.1'
    f1 = '1905.1'
    f2 = '1935.3'
    f3 = '1950.1'
    f4 = '2125.3'
    f5 = '2140.1'

    if len(bf) == 2:
        bf1 = bf[0].split(";")[5]
        bf2 = bf[0].split(";")[6]
        bf3 = bf[1].split(";")[5]
        bf4 = bf[1].split(";")[6]
        if bf1 == f2 and bf2 == f3 and bf3 == f4 and bf4 == f5:
            lae = ae.split(";")
            lae[2] = ""
            id = lae[3]
            res.append(';'.join(lae).strip())
            lbf1 = 'BF;;A;;;1935.3;1950.1;M;MXA;'
            lbf2 = 'BF;;A;;;2125.3;2140.1;M;MXA;'
            lem = em.split(";")
            lem[2] = "A"
            lem[3] = ""
            lem[4] = ""
            lem[5] = "119"
            lem[7] = "14M8D2WEW"
            res.append(';'.join(lem).strip())
            res.append(lbf1)
            res.append(lbf2)
            dct[id] = res
    elif len(bf) == 3:
        bf1 = bf[0].split(";")[5]
        bf2 = bf[0].split(";")[6]
        bf3 = bf[1].split(";")[5]
        bf4 = bf[1].split(";")[6]
        bf5 = bf[2].split(";")[5]
        bf6 = bf[2].split(";")[6]
        if bf1 == f0 and bf2 == f1 and bf3 == f2 and bf4 == f3 and bf5 == f4 and bf6 == f5:
            lae = ae.split(";")
            lae[2] = ""
            id = lae[3]
            res3.append(';'.join(lae).strip())
            lbf1 = 'BF;;A;;;1935.3;1950.1;M;MXA;'
            lbf2 = 'BF;;A;;;2125.3;2140.1;M;MXA;'
            lem = em.split(";")
            lem[2] = "A"
            lem[3] = ""
            lem[4] = ""
            lem[5] = "119"
            lem[7] = "14M8D2WEW"
            res3.append(';'.join(lem).strip())
            res3.append(lbf1)
            res3.append(lbf2)
            dct3[id] = res3
    else:
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
    with open(filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 4):
            if line[0:2] == "AE":
                if (line).split(";")[3] == "":
                    reject_file(filename, "ID empty ")
                    break
            if line[0:2] == "EM":
                if float((line).split(";")[8]) < 30 or float((line).split(";")[8]) > 36:
                    reject_file(filename, "In EM freq lt 30.0 or gt 36.0")
                    break


def pre_process(filename):
    with open(filename) as f:
        lines = f.readlines()
        BF = [item for item in lines if item[0:2] == "BF"]
        EN = [item for item in lines if item[0:2] == "EN"]

        #    for i,line in enumerate(lines,4):
        #        if line[0:2] == "AE" :
        #            if lines[i][0:2] != "EM" :
        #                reject_file(filename, "NO BF or no EN or not starting with AE or EM pb")
        #                return False

        if len(BF) == 0 or len(EN) == 0:
            reject_file(filename, "NO BF or no EN ")
            return False
        else:
            logging.info('Pre_processing OK for file : ' + filename.name)
            return True


def process(filename):
    header = []
    footer = []
    out_filename = dirout/filename.name

    bf = []
    dn = []
    sem = ""
    # res=[]
    dct.clear()
    dct3.clear()
    i_en = 0
    idx = 0
    with open(filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i < 4:
                header.append(line.strip())
            if line[0:2] == "AE":
                if len(bf) > 0:
                    is_valide(sae, sem, bf)
                    validate(sae, sem, bf, dct)
                    sae = line
                    bf = []
                else:
                    sae = line
                    bf = []

            if line[0:2] == "EM":
                if len(bf) > 0:
                    validate(sae, sem, bf, dct)
                    sem = line
                    bf = []
                else:
                    sem = line
            if line[0:2] == "BF":
                bf.append(line.strip())
            if line[0:2] == "DN":
                continue
            if line[0:2] == "SA":
                if len(bf) > 0:
                    validate(sae, sem, bf, dct)
                footer.append(line.strip())
            if line[0:2] == "ES":
                es = line.strip()
                les = es.split(";")
                if les[2] == "S":
                    footer.append(es)
                else:
                    if les[10] == "":
                        y = round(random.uniform(0.6, 1.01), 2)
                        les[10] = str(y)
                        footer.append(';'.join(les).strip())
            if line[0:2] == "EN":
                footer.append(line.strip())
    if len(dct) > 0:
        with open(out_filename, 'w') as out_file:
            for i in range(0, len(header)):
                out_file.write('%s\n' % header[i])
            for key, value in dct.items():
                for i in range(0, len(value)):
                    out_file.write('%s\n' % value[i])
            for i in range(0, len(dn)):
                out_file.write('%s\n' % dn[i])
            for i in range(0, len(footer)):
                out_file.write('%s\n' % footer[i])
    elif len(dct3) > 0:
        with open(out_filename, 'w') as out_file:
            for i in range(0, len(header)):
                out_file.write('%s\n' % header[i])
            for key, value in dct3.items():
                for i in range(0, len(value)):
                    out_file.write('%s\n' % value[i])
            for i in range(0, len(dn)):
                out_file.write('%s\n' % dn[i])
            for i in range(0, len(footer)):
                out_file.write('%s\n' % footer[i])

    else:
        reject_file(filename, "0 valid BF")


logging.info('Start files processing  directory input : ' + dirpath.name)
logging.info('Start files processing  directory output : ' + dirout.name)
i_zip = 0
i_txt = 0
for f in dirpath.iterdir():
    if (f.name).endswith(".zip"):
        i_zip += 1
        logging.info('unzip file  : ' + f.name)
        print(f)
        shutil.unpack_archive(f, dirpath, 'zip')
for f in dirpath.iterdir():
    if (f.name).endswith(".txt"):
        i_txt += 1
        logging.info('pre_process file ===>  : ' + f.name)
        #res = pre_process(f)
        if pre_process(f) == True:
            process(f)
        else:
            continue
logging.info('End processing of : ' + str(i_zip) +
             ' zip files to :' + str(i_txt) + ' txt files')
for f in dirout.iterdir():
    if (f.name).endswith(".txt"):
        logging.info('Post_process file ===>  : ' + f.name)
        post_process(f)
logging.info('End Post processing')

"""
activate to zip file in out directory
for f in dirout.iterdir():  
    if (f.name).endswith(".txt"):
        zipfile=((f.name).split(".")[0])+'.zip'
        logging.info('zip  file ===>  : '+ f.name)
        print(f)
        print(zipfile)
        with ZipFile(str(dirout)+ '/'+zipfile, 'w') as myzip:
            myzip.write(str(f),basename(str(f)))
            if os.path.exists(str(f)): os.remove(str(f))
    else : continue

"""

logging.info('End Zip ')
