import os,sys

import multiprocessing
from multiprocessing import Process
from optparse import OptionParser
import time


def gen_dict(prot_file):
    prot_dict={}

    #convert protein fasta file to python dictionary
    with open(prot_file,'r') as fd_prot:
        content=''
        prot_seq=[]
        prot_name=[]
        while True:
            line = fd_prot.readline().rstrip()
            if not line:
                prot_seq.append(content)
                prot_dict = dict(zip(prot_name,prot_seq))
                break
            if line.startswith(">"):
                prot_name.append(line)
                if not content == "":
                    prot_seq.append(content)
                    content=""
            else:
                content = content + line
    
    return prot_dict
 
### The multi-threads DNAworks function
def dnaworks_proc(item,index,outfasta,outdna,cap_sequence,tail_sequence,codon):

    inp="tmp"+str(index)+".inp"
    logname="ID"+str(index)+".dna"
    with open(inp,'a') as tmp:
    #specify the directives of DNAworks. you can specify your custom directives by changing the fllowing lines
        tmp.write('title '+"sample"+"\n")
        tmp.write("logfile "+ logname + "\n")
        #tmp.write("length low 180\n")
        tmp.write("codon " + codon +"\n")
        tmp.write("protein\n")
        tmp.write(" " + item[1] + "\n //")
    #run DNAworks    
    os.system("dnaworks %s" %inp)
    os.system("rm %s" %inp)
    #extract DNA sequence of DNAworks ouput
    flag=0
    text=''
    with open(logname,"r") as fd_log:
        for line in fd_log:
            if "The DNA sequence" in line:
                flag=1
            if "The oligonucleotide assembly" in line:
                break
            if flag == 1 and "The DNA sequence" not in line and "-----" not in line:
                text+=line.strip()
    result=filter(lambda ch: ch not in ' \t1234567890', text)
    result="".join(list(result))
    
    #specify homologous sequence
    cap_sequence=filter(lambda ch: ch not in ' \t1234567890', cap_sequence)
    cap_sequence="".join(list(cap_sequence))

    tail_sequence=filter(lambda ch: ch not in ' \t1234567890', tail_sequence)
    tail_sequence="".join(list(tail_sequence))
    
    #
    print("process:DNAWORKS %s finished" %str(item[0])," :%s" %result)
    with open(outfasta,"a") as out_fasta,open(outdna,"a") as out_dna:
        out_fasta.write(str(item[0])+"\n"+str(cap_sequence).upper()+result.upper()+str(tail_sequence).upper()+"\n")
        out_dna.write(str(cap_sequence).upper()+result.upper()+str(tail_sequence).upper()+"\n")
    os.system("rm %s" %logname)


############### main #################
if __name__ == "__main__":

    parser = OptionParser(usage="%prog [options] -i <input fasta file> -j <number of processes to use> -a <output fasta file> -d <output DNA list>",
                description=__doc__)

    parser.add_option("-i","--input",
            action="store",
            dest="inputfile",
            help="input fasta file")

    parser.add_option("-j","--nproc",
            action="store",
            dest="Nproc",
            default="1",
            help="Number of processes to be started. The capacity of multiprocessing pool. Default=1")
    
    parser.add_option("--codon","--codon",
            action="store",
            dest="codon",
            default="E. coli",
            help="codon [ ecoli2 | E. coli | C. elegans | D. melanogaster | H. sapiens | 
     M. musculus | R. novegicus | S. cerevesiae | X. laevis | P. pastoris ] Defualt=E. coli")
    

    parser.add_option("-c","--cap",
            action="store",
            dest="cap_sequence",
            default="",
            help="The homologous sequence at the 5'-terminal. Default=None")

    parser.add_option("-t","--tail",
            action="store",
            dest="tail_sequence",
            default="",
            help="The homologous sequence at the 3'-terminal. Default=None")

    parser.add_option("-a","--out_fasta",
            action="store",
            dest="outfasta",
            default="out.fasta",
            help="Write output file in fasta format. Default=out.fasta")

    parser.add_option("-d","--out_dna",
            action="store",
            dest="outdna",
            default="out.dna",
            help="Write dna sequences in a list. Default=out.dna")

    parser.add_option("-g","--log",
            action="store",
            dest="logfile",
            default="log",
            help="Inputs information to be stored. Default=log")

    (options, args) = parser.parse_args()
    inputfile = options.inputfile
    Nproc = int(options.Nproc)
    outfasta = options.outfasta
    outdna = options.outdna
    cap_sequence = options.cap_sequence
    tail_sequence = options.tail_sequence
    logfile = options.logfile
    codon = options.codon
    
    try:
        localday = time.strftime("%Y-%m-%d", time.localtime())
        localtime = time.strftime("%H:%M:%S", time.localtime())
        prot_dict=gen_dict(inputfile)

        with open(logfile,"w") as fd_log:
            fd_log.write("Job started on %s at %s" %(localday,localtime) +"\n\n")
            fd_log.write("Input file name: %s" %inputfile +"\n")
            fd_log.write("Number of sequences to be processes: %s" %len(prot_dict) +"\n")
            fd_log.write("Number of processes to be used: %s" %Nproc +"\n")
            fd_log.write("5' homologous sequence: %s" %cap_sequence +"\n")
            fd_log.write("3' homologous sequence: %s" %tail_sequence +"\n")
            fd_log.write("\n......\n\n")

        pool = multiprocessing.Pool(Nproc)
        for index,item in enumerate(prot_dict.items()):
            pool.apply_async(dnaworks_proc,(item,index,outfasta,outdna,cap_sequence,tail_sequence,))
        
        pool.close()
        pool.join()
        
        localday = time.strftime("%Y-%m-%d", time.localtime())
        localtime = time.strftime("%H:%M:%S", time.localtime())

        with open(logfile,"a") as fd_log:
            fd_log.write("Output fasta file: %s" %outfasta +"\n")
            fd_log.write("Output dna list: %s" %outdna +"\n\n")
            fd_log.write("Job finished on %s at %s" %(localday,localtime) +"\n")
  
    except:
        parser.error("Bad directives.\n\nPlease check your input files.\nSee more information by using -h or --help")




