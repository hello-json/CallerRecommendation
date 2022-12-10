# -*- coding: UTF-8 -*-
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--the_vcf', help='the vcf Result of SV software', required=True, type=str)
parser.add_argument('-a', '--the_stander', help='the standard Answer', required=True, type=str)  #stander单词应该是standard，将错就错了。不过其实stander本身也有标准的意思，是名词。
args = parser.parse_args()
vcfFile = args.the_vcf
standerFile = args.the_stander

chromosomesCodingDic = {"chr1": 1000000000, "chr2": 2000000000, "chr3": 3000000000, "chr4": 4000000000, "chr5": 5000000000, "chr6": 6000000000, "chr7": 7000000000, "chr8": 8000000000, "chr9": 9000000000, "chr10": 10000000000, "chr11": 11000000000, "chr12": 12000000000, "chr13": 13000000000, "chr14": 14000000000, "chr15": 15000000000, "chr16": 16000000000, "chr17": 17000000000, "chr18": 18000000000, "chr19": 19000000000, "chr20": 20000000000, "chr21": 21000000000, "chr22": 22000000000, "chrX": 23000000000, "chrY": 24000000000, "chrM": 25000000000, "1": 1000000000, "2": 2000000000, "3": 3000000000, "4": 4000000000, "5": 5000000000, "6": 6000000000, "7": 7000000000, "8": 8000000000, "9": 9000000000, "10": 10000000000, "11": 11000000000, "12": 12000000000, "13": 13000000000, "14": 14000000000, "15": 15000000000, "16": 16000000000, "17": 17000000000, "18": 18000000000, "19": 19000000000, "20": 20000000000, "21": 21000000000, "22": 22000000000, "X": 23000000000, "Y": 24000000000, "M": 25000000000}
typeCodingDic = {"INS":100000000000, "DEL":200000000000, "DUP":300000000000, "INV":400000000000, "BND":500000000000}   #增添处

vcf_object = open(vcfFile)
try:
     vcf_file = vcf_object.read( )
finally:
     vcf_object.close( )
vcf_file_rows = vcf_file.split('\n')
prediction = []
for vcf_file_row in vcf_file_rows:
    if not vcf_file_row.startswith('#'):
        try:
            this_type = vcf_file_row.split('SVTYPE=')[1][:3]   #增添处
            prediction.append(typeCodingDic[this_type] + chromosomesCodingDic[vcf_file_row.split('\t')[0]] + int(vcf_file_row.split('\t')[1]))   #改动处
        except:
            continue

stander_object = open(standerFile)
try:
     stander_file = stander_object.read( )
finally:
     stander_object.close( )
stander_file_rows = stander_file.split('\n')
answer = []
for stander_file_row in stander_file_rows:
    if not stander_file_row.startswith('#'):
        try:
            this_type = stander_file_row.split('SVTYPE=')[1][:3]   #增添处
            answer.append(typeCodingDic[this_type] + chromosomesCodingDic[stander_file_row.split('\t')[0]] + int(stander_file_row.split('\t')[1]))   #改动处
        except:
            continue

#判断约等函数开始
def ifSame(site1, site2):
    theSubtractThreshold = 10
    if abs(int(site1) - int(site2)) < theSubtractThreshold:
        return True
    else:
        return False
#判断约等函数结束

#评价指标计算函数开始
def caculate(answer, prediction):
    call = len(prediction)
    ref = len(answer)
    TP = 0
    for prediction_element in prediction:
        for answer_element in answer:
            if ifSame(answer_element, prediction_element):
                TP = TP + 1
    try:
        Precision = float(TP) / float(call)
    except:
        Precision = 0
    try:
        Recall = float(TP) / float(ref)
    except:
        Recall = 0
    try:
        F_measure = float(2 * Precision * Recall) / float(Precision + Recall)
    except:
        F_measure = 0
    print "Precision:" + str(Precision)
    print "Recall:" + str(Recall)
    print "F_measure:" + str(F_measure)
#评价指标计算函数结束

caculate(answer, prediction)
