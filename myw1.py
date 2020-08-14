import os
import zipfile
import random
out_filename = ".//out.txt"
filename = ".//mytst2.txt"
directoryIn = './/in//'
directoryOut = './/out//'


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

    
    
    
def process(path,filename,outpath):
    header=[]
    footer=[]
    out_filename =  outpath + filename+".out"
    filename= path + filename

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
                    if les[10] == "":
                        y=round(random.uniform(0.6,1.2),2)
                        les[10]=str(y)
                    print(';'.join(les))
                    footer.append(';'.join(les).strip())
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
for filename in os.listdir(directoryIn):
    if filename.endswith(".zip"):
        with zipfile.ZipFile(directoryIn+filename, 'r') as myzip:
            myzip.extractall(directoryIn)
    if filename.endswith(".txt"):
        print(filename)
        process(directoryIn,filename,directoryOut)    
