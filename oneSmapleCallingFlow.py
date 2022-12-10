# -*- coding: UTF-8 -*-
import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--the_inputFq', help='the inputFq, eg:/mnt/X500/farmers/wangshj/realData/HG002/fq/m54238_180901_011437.Q20.fastq', required=True, type=str)
parser.add_argument('-o', '--the_outPutDir', help='the outPutDir, eg:/mnt/X500/farmers/wangshj/realData/HG002/fq/HG002CallingResult/, 注意最后的这个斜杠一定要写上', required=True, type=str)
args = parser.parse_args()
inputFq = args.the_inputFq
nowDir = args.the_outPutDir

feature = "tmpFeatureName"
oneGraName = "tmpGraName"
os.system("mkdir " + nowDir)
os.system("mkdir " + nowDir + "test" + feature)
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName)
os.system("ln -s " + inputFq + " " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq")
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName + "/picky")
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv")
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv")
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles")
os.system("mkdir " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv")
    
#生成picky运行命令开始
shellName_inPickySrc = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.sh'
pickyRunningShell = open('/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/softWare/picky/Picky-0.2.a/src/' + shellName_inPickySrc, 'w')
pickyRunningShell.write("# general installation" + "\n" +  "export LASTAL=/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/theLAST/bin/lastal" + "\n" + "export PICKY=/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/softWare/picky/Picky-0.2.a/src/picky.pl" + "\n" +  "# general configuration" + "\n" +  "export LASTALDB=/mnt/X500/farmers/wangshj/refGenome/hg19.lastdb" + "\n" +  "export LASTALDBFASTA=/mnt/X500/farmers/wangshj/refGenome/hg19.fa" + "\n" +  "export NTHREADS=10" + "\n" + "# FASTQ file" + "\n" + "export RUN=" + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001" + "\n" + "# reads alignments" + "\n" + "time (${LASTAL} -C2 -K2 -r1 -q3 -a2 -b1 -v -v -P${NTHREADS} -Q1 ${LASTALDB} ${RUN}.fastq 2>${RUN}.lastal.log | ${PICKY} selectRep --thread ${NTHREADS} --preload 6 1>${RUN}.align 2>${RUN}.selectRep.log)" + "\n" + "# call SVs" + "\n" + "time (cat ${RUN}.align | ${PICKY} callSV --oprefix ${RUN} --fastq ${RUN}.fastq --genome ${LASTALDBFASTA} --exclude=chrM --sam)" + "\n" + "# generate VCF format" + "\n" + "${PICKY} xls2vcf --xls ${RUN}.profile.DEL.xls --xls ${RUN}.profile.INS.xls --xls ${RUN}.profile.INDEL.xls --xls ${RUN}.profile.INV.xls --xls ${RUN}.profile.TTLC.xls --xls ${RUN}.profile.TDSR.xls --xls ${RUN}.profile.TDC.xls > ${RUN}.allsv.vcf" + "\n")
pickyRunningShell.close()
pickyComand1 = "sh /mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/softWare/picky/Picky-0.2.a/src/" + shellName_inPickySrc
pickyComand2 = "mv " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.allsv.vcf " + nowDir + "test" + feature + "/" + oneGraName + "/picky"
pickyComand3 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.profile*"
pickyComand4 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.align " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.lastal.log " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.selectRep.log"
pickyComand5 = "rm /mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/softWare/picky/Picky-0.2.a/src/" + shellName_inPickySrc
pickyComand6 = "mv " + nowDir + "test" + feature + "/" + oneGraName + "/picky/sd_0001.allsv.vcf " + nowDir + "test" + feature + "/" + oneGraName + "/picky/picky.vcf"
pickyShell = open(nowDir + 'picky.sh', 'w')
pickyShell.write(pickyComand1 + "\n" +  pickyComand2 + "\n" + pickyComand3 + "\n" +  pickyComand4 + "\n" +  pickyComand5 + "\n" +  pickyComand6)
pickyShell.close()
#生成picky运行命令结束

#生成nanosv运行命令开始
nanosvComand1 = "minimap2 -t 10 -ax map-pb /mnt/X500/farmers/wangshj/refGenome/hg19.fa " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq > " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.sam"
nanosvComand2 = "samtools view -bS " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.sam > " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.bam"
nanosvComand3 = "samtools sort " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.bam > " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp_sort.bam"
nanosvComand4 = "samtools index " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp_sort.bam"
nanosvComand5 = "bedtools bamtobed -i " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp_sort.bam > " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.bed"
nanosvComand6 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/svim_env/bin/NanoSV -t 10 -s /mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/theSAMBAMBA/bin/sambamba -b " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp.bed " + "-o " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/nanosv.vcf " +  nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp_sort.bam"
nanosvComand7 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv/tmp*"
nanosvShell = open(nowDir + 'nanosv.sh', 'w')
nanosvShell.write(nanosvComand1 + "\n" +  nanosvComand2 + "\n" + nanosvComand3 + "\n" +  nanosvComand4 + "\n" +  nanosvComand5 + "\n" +  nanosvComand6 + "\n" +  nanosvComand7)
nanosvShell.close()
#生成nanosv运行命令结束

#生成pbsv运行命令开始
pbsvComand1 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/thePBMM2/bin/pbmm2 align /mnt/X500/farmers/wangshj/refGenome/hg19.fa " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/ref.movie1.bam -j 1 --sort --sample sample1 --rg " + "\'" + "@RG" + "\\" + "tID:movie1" + "\'"
pbsvComand2 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/thePBSV/bin/pbsv discover " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/ref.movie1.bam " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/ref.sample1.svsig.gz"
pbsvComand3 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/thePBSV/bin/pbsv call /mnt/X500/farmers/wangshj/refGenome/hg19.fa " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/ref.sample1.svsig.gz " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/pbsv.vcf -j 1"
pbsvComand4 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv/ref*"
pbsvShell = open(nowDir + 'pbsv.sh', 'w')
pbsvShell.write(pbsvComand1 + "\n" +  pbsvComand2 + "\n" + pbsvComand3 + "\n" +  pbsvComand4)
pbsvShell.close()
#生成pbsv运行命令结束

#生成sniffles运行命令开始
#snifflesComand1 = "bwa mem -M -t 50 /products/repos/prod/Akso/BNC/program/NoahCare/db/alignment/tgp_phase2_flat/hs37d5.fa " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq > " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.sam"
snifflesComand1 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/theNGMLR/bin/ngmlr -t 10 -r /mnt/X500/farmers/wangshj/refGenome/hg19.fa -q " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq -o " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.sam"
snifflesComand2 = "python " + nowDir + "helpSnifflesToBam.py -i " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.sam" + " -o " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.sam"
snifflesComand3 = "samtools view -bS " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.sam > " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.bam"
snifflesComand4 = "samtools sort " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp.bam > " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp_sort.bam"
snifflesComand5 = "samtools index " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp_sort.bam"
snifflesComand6 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/theSNIFFLES/bin/sniffles -m " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp_sort.bam -v " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/sniffles.vcf"
snifflesComand7 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles/tmp*"
snifflesShell = open(nowDir + 'sniffles.sh', 'w')
snifflesShell.write(snifflesComand1 + "\n" +  snifflesComand2 + "\n" + snifflesComand3 + "\n" +  snifflesComand4 + "\n" +  snifflesComand5 + "\n" +  snifflesComand6 + "\n" +  snifflesComand7)
snifflesShell.close()
#生成sniffles运行命令结束

#生成cutesv运行命令开始
cutesvComand1 = "minimap2 -t 10 -ax map-pb /mnt/X500/farmers/wangshj/refGenome/hg19.fa " + nowDir + "test" + feature + "/" + oneGraName + "/sd_0001.fastq > " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp.sam"
cutesvComand2 = "samtools view -bS " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp.sam > " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp.bam"
cutesvComand3 = "samtools sort " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp.bam > " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp_sort.bam"
cutesvComand4 = "samtools index " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp_sort.bam"
cutesvComand5 = "/mnt/X500/farmers/wangshj/softWare/bioconda/smallEvironment/theCUTESV/bin/cuteSV " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp_sort.bam /mnt/X500/farmers/wangshj/refGenome/hg19.fa " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/cutesv.vcf " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/"
cutesvComand6 = "rm " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv/tmp*"
cutesvShell = open(nowDir + 'cutesv.sh', 'w')
cutesvShell.write(cutesvComand1 + "\n" +  cutesvComand2 + "\n" + cutesvComand3 + "\n" +  cutesvComand4 + "\n" +  cutesvComand5 + "\n" +  cutesvComand6)
cutesvShell.close()
#生成cutesv运行命令开始

#将几个软件运行命令汇总入一个脚本开始
allSvCallerShell = open(nowDir + 'allSvCaller.sh', 'w')
allSvCallerShell.write("sh " + nowDir + "picky.sh" + "\n" + "sh " + nowDir + "nanosv.sh" + "\n" + "sh " + nowDir + "pbsv.sh" + "\n" + "sh " + nowDir + "sniffles.sh" + "\n" + "sh " + nowDir + "cutesv.sh")
allSvCallerShell.close()
#将几个软件运行命令汇总入一个脚本结束

os.system("sh " + nowDir + "allSvCaller.sh")

#os.system("rm " + nowDir + "cutesv.sh nanosv.sh pbsv.sh picky.sh sniffles.sh allSvCaller.sh")
os.system("rm " + "cutesv.sh nanosv.sh pbsv.sh picky.sh sniffles.sh allSvCaller.sh")

os.system("mv " + nowDir + "test" + feature + "/" + oneGraName + "/nanosv " + nowDir + "test" + feature + "/" + oneGraName + "/picky " + nowDir + "test" + feature + "/" + oneGraName + "/sniffles " + nowDir + "test" + feature + "/" + oneGraName + "/pbsv " + nowDir + "test" + feature + "/" + oneGraName + "/cutesv " + nowDir)

#print "rm -rf " + nowDir + "test" + feature
#os.system("rm -rf " + nowDir + "test" + feature) #这行代码一定要小心！！！！！！
os.system("rm -rf " + "test" + feature)
