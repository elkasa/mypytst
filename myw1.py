import shutil
import random
import logging
import pathlib 



current_dir=pathlib.Path.cwd()
logging.basicConfig(filename='logfile.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

dirpath = pathlib.Path.cwd()/'in'
dirout=pathlib.Path.cwd()/'out'
dirrejet=pathlib.Path.cwd()/'rejet'
raison =""
assert(dirpath.is_dir())
assert(dirout.is_dir())
assert(dirrejet.is_dir())

def is_valide(ae,em,bf):
    if ae == "":
        return False
    elif em == "":
        return False
    elif ae.split(";")[3] == "":
        return False
    elif float(em.split(";")[8]) < 30 :
        return False
    else:
        return True
        

def validate(ae,em,bf,res):
    if len(bf) == 2 :
        bf1=bf[0].split(";")[5]
        bf2=bf[0].split(";")[6]
        if bf[0].split(";")[5] == '1935.3' and bf[0].split(";")[6] == '1950.1' and bf[1].split(";")[5] == '2125.3' \
            and bf[1].split(";")[6] == '2140.1':
            lae=ae.split(";")
            lae[2]=""
            res.append(';'.join(lae).strip())
            lem=em.split(";")
            lem[4]=""
            lem[5]="119"
            lem[7]="14M8D2WEW"
            res.append(';'.join(lem).strip())
            res.append(bf[0])
            res.append(bf[1])
        else:
            pass
    else:
        pass
    return res


def reject_file(filename, raison ):
                fname=filename.name
                logging.error('This file is rejected KO raison  '+ raison  + fname)
                shutil.move(filename, dirrejet/fname)                
                zipfile=(fname.split(".")[0])+'.zip'
                fl=pathlib.Path(dirpath/zipfile)
                if fl.is_file():
                    shutil.move(fl, dirrejet/zipfile)
                    logging.error('This file is rejected KO : ' +  zipfile)
                    
def post_process(filename):
    with open(filename) as f:
        lines=f.readlines()
        for i,line in enumerate(lines,4):
            if line[0:2] == "AE":
                if (line).split(";")[3] == "": 
                    reject_file(filename, "ID empty ")
                    break
            if line[0:2] == "EM": 
                if float((line).split(";")[8]) < 30 : 
                    reject_file(filename, "In EM freq lt 30.0 .")
                    break
                


def pre_process(filename):
    with open(filename) as f:
            lines=f.readlines()
            BF=[item for item in lines if item[0:2] == "BF"]
            EN=[item for item in lines if item[0:2] == "EN"]
            
            for i,line in enumerate(lines,4):
                if line[0:2] == "AE" :
                    if lines[i][0:2] != "EM" : 
                        reject_file(filename, "NO BF or no EN or not starting with AE or EM pb")
                        break
            
            if len(BF) == 0 or len(EN) == 0 or lines[4][0:2] != "AE" or lines[5][0:2] != "EM":
                reject_file(filename, "NO BF or no EN or not starting with AE or EM pb")
                return False
            else:
                logging.info('Pre_processing OK for file : ' + filename.name)
                return True
                

def process(filename):
    header=[]
    footer=[]
    out_filename =  dirout/filename.name
    

    bf=[]
    dn=[]
    sem=""
    res=[]
    i_en = 0
    idx = 0
    with open(filename) as f:
            lines=f.readlines()
            for i,line in enumerate(lines):
                if i < 4 :header.append(line.strip())
                if line[0:2] == "AE":
                    if len(bf) > 0:
                        is_valide(sae,sem,bf)
                        validate(sae,sem,bf,res)
                        sae=line
                        bf=[]
                    else:
                        sae=line
                        bf=[]

                if line[0:2] == "EM": 
                    if len(bf) > 0:
                        validate(sae,sem,bf,res)
                        sem=line
                        bf=[]
                    else:
                        sem=line
                if line[0:2] == "BF": bf.append(line.strip())
                if line[0:2] == "DN": continue
                if line[0:2] == "SA": footer.append(line.strip())
                if line[0:2] == "ES":
                    es=line.strip()
                    les= es.split(";")
                    if les[2] =="S":
                        footer.append(es)
                    else:
                        if les[10] == "":
                            y=round(random.uniform(0.6,1.2),2)
                            les[10]=str(y)
                            footer.append(';'.join(les).strip())
                    #footer.append(es)
                if line[0:2] == "EN":
                    i_en +=1
                    if len(bf) > 0:
                        validate(sae,sem,bf,res)
                        bf=[]
                    if i_en < 3 :
                        footer.append(line.strip())
                    else:
                        continue

    with open(out_filename, 'w') as out_file:
        for i in range (0,len(header)):
            out_file.write('%s\n' % header[i])
        for i in range (0,len(res)):
            out_file.write('%s\n' % res[i])
        for i in range (0,len(dn)):
            out_file.write('%s\n' % dn[i])
        for i in range (0,len(footer)):
            out_file.write('%s\n' % footer[i])



logging.info('Start files processing  directory input : '+ dirpath.name)
logging.info('Start files processing  directory output : '+ dirout.name)
i_zip = 0
i_txt = 0
for f in dirpath.iterdir():
    if (f.name).endswith(".zip"):
        i_zip +=1
        logging.info('unzip file  : '+ f.name)
        shutil.unpack_archive(f,dirpath)
for f in dirpath.iterdir():
    if (f.name).endswith(".txt"):
        i_txt += 1
        logging.info('pre_process file ===>  : '+ f.name)
        res = pre_process(f) 
        if res == True :
            process(f)
        else:
            continue
logging.info('End processing of : ' + str(i_zip) + ' zip files to :'+ str(i_txt) + ' txt files')           
for f in dirout.iterdir():
    if (f.name).endswith(".txt"):
        logging.info('Post_process file ===>  : '+ f.name)
        post_process(f)
logging.info('End Post processing')
