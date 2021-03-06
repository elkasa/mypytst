import shutil
import random
import logging
import pathlib
from zipfile import ZipFile
import os
from os.path import basename


'''
version v2.0
27/08 
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

data = dict()
data3 = dict()
header = []
footer = []


"""
pre process
"""


def pre_process(filename):
    with open(filename) as f:
        lines = f.readlines()
        EM = [item for item in lines if item[0:2] == "EM"]
        BF = [item for item in lines if item[0:2] == "BF"]
        AE = [item for item in lines if item[0:2] == "AE"]

        if len(BF) == 0 or len(AE) == 0 or len(EM) == 0:
            reject_file(filename, "0 BF or no 0 EM or 0 AE ")
            return False
        else:
            logging.info('Pre_processing OK for file : ' + filename.name)
            return True


"""
func validate
"""


def validate(ae, em, bf):
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
            data[id] = res
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
            data3[id] = res3
    else:
        pass


"""
end validate
"""

"""
func rejet file
"""


def reject_file(filename, raison):
    fname = filename.name
    logging.error('This file is rejected KO raison  ' + raison + fname)
    shutil.move(filename, dirrejet/fname)
    zipfile = (fname.split(".")[0])+'.zip'
    fl = pathlib.Path(dirpath/zipfile)
    if fl.is_file():
        shutil.move(fl, dirrejet/zipfile)
        logging.error('This file is rejected KO : ' + zipfile)


"""
end reject file
"""

"""
post_process
"""


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


"""
end post_process
"""


"""
    Process func
    """


def process(filename):
    # header = []
    # footer = []
    bf = []
    i_en = 0
    # data.clear()
    # data3.clear()

    with open(filename) as f:
        line = f.readline()
        header.append(line.strip())
        line = f.readline()
        header.append(line.strip())
        line = f.readline()
        header.append(line.strip())
        line = f.readline()
        header.append(line.strip())
        print(len(header))
        while line:
            if line[0:2] == 'AE':
                ae = line
                # print("ae")
            if line[0:2] == 'EM':
                em = line
                # print("em")
            if line[0:2] == 'BF':
                bf = []
                while line[0:2] == 'BF':
                    bf.append(line.strip())
                    # print("===bf")
                    line = f.readline()
                validate(ae, em, bf)
                continue
            if line[0:2] == "DN":
                pass
            if line[0:2] == "SA":
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

            line = f.readline()


"""
end func process
"""

"""
    write out data
    """


def write_out(filename):
    out_filename = dirout/filename.name

    if len(data) > 0:
        with open(out_filename, 'w') as out_file:
            for i in range(0, len(header)):
                out_file.write('%s\n' % header[i])
            for _, value in data.items():
                for i in range(0, len(value)):
                    out_file.write('%s\n' % value[i])
            for i in range(0, len(footer)):
                out_file.write('%s\n' % footer[i])
    elif len(data3) > 0:
        with open(out_filename, 'w') as out_file:
            for i in range(0, len(header)):
                out_file.write('%s\n' % header[i])
            for _, value in data3.items():
                for i in range(0, len(value)):
                    out_file.write('%s\n' % value[i])
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
        shutil.unpack_archive(f, dirpath, 'zip')

for f in dirpath.iterdir():
    if (f.name).endswith(".txt"):
        i_txt += 1
        logging.info('process file ===>  : ' + f.name)
        header = []
        footer = []
        data.clear()
        data3.clear()
        if pre_process(f) == True:
            process(f)
            write_out(f)
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
