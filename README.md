# CallerRecommendation
Experiment
Experiment running example:
(Picky)  theLAST/bin/lastdb -v -P 1 hg19.lastdb hg19.fa
samtools dict -H hg19.fa > hg19.seq.dict
picky/Picky-0.2.a/src/picky.pl script --fastq LongRead.fastq --thread 1 > run.sh
       Let “theLAST/bin/lastal”, “picky/Picky-0.2.a/src/picky.pl”, “/refGenome/hg19.lastdb” and “/refGenome/hg19.fa” in “export LASTAL=”，“export PICKY=”，“export LASTALDB=” and “export LASTALDBFASTA=”.
(NanoSV)  bedtools bamtobed -i sor.bam > sor.bed
/svim_env/bin/NanoSV -t 1 -s /theSAMBAMBA/bin/sambamba -b sor.bed -o sor.vcf sor.bam
(pbsv) /thePBMM2/bin/pbmm2 align /refGenome/hg19.fa movie1.Q20.fastq ref.movie1.bam --sort  --sample sample1 --rg '@RG\tID:movie1'  or
    /thePBMM2/bin/pbmm2 align /refGenome/hg19.fa movie1.Q20.fastq ref.movie1.bam --sort --preset CCS --sample sample1 --rg '@RG\tID:movie1'
/thePBSV/bin/pbsv discover ref.movie1.bam ref.sample1.svsig.gz
/thePBSV/bin/pbsv call /refGenome/hg19.fa ref.sample1.svsig.gz ref.var.vcf
（sniffles）
/theNGMLR/bin/ngmlr -t 1 -r /refGenome/hg19.fa -q sor.fastq -o sor.sam or
bwa mem -M -t 1 /refGenome/hg19.fa sor.fastq > sor.sam
samtools view -bS sor.sam > sor.bam
samtools sort sor.bam > sort_sor.bam
samtools index sort_sor.bam
/theSNIFFLES/bin/sniffles -m sort_sor.bam -v output.vcf
(cutesv) /theCUTESV/bin/cuteSV sort_sor.bam /refGenome/hg19.fa sor.vcf /theCUTESV/testData/

Recommendation
Installation-free mode, copy the code directly and run the following command.
Recommendation running example:
python newSampleRecommend.py -f sample.fq
Then, the recommendation results will be printed in the console.
