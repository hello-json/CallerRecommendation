# -*- coding: UTF-8 -*-
import argparse
import os
from sklearn.externals import joblib

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fq_file', help='input the fq file', required=True, type=str)
args = parser.parse_args()
fqFile = args.fq_file


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def ref_span(cigar_arr):
    sss = 0
    for iii in cigar_arr:
        if iii[-1] == "M" or iii[-1] == "D":
            sss = sss + int(iii[:-1])
    return sss

os.system("minimap2 -t 10 -a hg19.fa " + fqFile + " > tmp.sam")
print "比对已完成"

this_samFile = "tmp.sam"
this_samFile_obj = file(this_samFile,'r')
this_samFile_arr1 = []
this_samFile_readID_maxMapQul_dic = {}
for oneSamLine in this_samFile_obj.readlines():
    if not oneSamLine.startswith('@'):
        oneSamLine_array = oneSamLine.split('\t')
        if oneSamLine_array[5] != "*" and int(oneSamLine_array[4]) >= 30 and "H" not in oneSamLine_array[5]:
            if this_samFile_readID_maxMapQul_dic.has_key(oneSamLine_array[0]):
                if int(oneSamLine_array[4]) > this_samFile_readID_maxMapQul_dic[oneSamLine_array[0]]:
                    this_samFile_readID_maxMapQul_dic[oneSamLine_array[0]] = int(oneSamLine_array[4])
            else:
                this_samFile_readID_maxMapQul_dic[oneSamLine_array[0]] = int(oneSamLine_array[4])
            this_samFile_arr1.append(oneSamLine_array)
print "第一步完成"

this_samFile_arr2 = []
for oneSamLine1 in this_samFile_arr1:
    if this_samFile_readID_maxMapQul_dic[oneSamLine1[0]] == int(oneSamLine1[4]):
        this_samFile_arr2.append(oneSamLine1)
this_samFile_arr1 = []
print "第二步完成"

chromosomesCodingDic = {"chr1": 1000000000, "chr2": 2000000000, "chr3": 3000000000, "chr4": 4000000000, "chr5": 5000000000, "chr6": 6000000000, "chr7": 7000000000, "chr8": 8000000000, "chr9": 9000000000, "chr10": 10000000000, "chr11": 11000000000, "chr12": 12000000000, "chr13": 13000000000, "chr14": 14000000000, "chr15": 15000000000, "chr16": 16000000000, "chr17": 17000000000, "chr18": 18000000000, "chr19": 19000000000, "chr20": 20000000000, "chr21": 21000000000, "chr22": 22000000000, "chrX": 23000000000, "chrY": 24000000000, "chrM": 25000000000, "1": 1000000000, "2": 2000000000, "3": 3000000000, "4": 4000000000, "5": 5000000000, "6": 6000000000, "7": 7000000000, "8": 8000000000, "9": 9000000000, "10": 10000000000, "11": 11000000000, "12": 12000000000, "13": 13000000000, "14": 14000000000, "15": 15000000000, "16": 16000000000, "17": 17000000000, "18": 18000000000, "19": 19000000000, "20": 20000000000, "21": 21000000000, "22": 22000000000, "X": 23000000000, "Y": 24000000000, "M": 25000000000}
sv_begin_arr = []
sv_end_arr = []
read_len_arr = []
for oneSamLine2 in this_samFile_arr2:
    chromosomes = oneSamLine2[2]
    if "_" in chromosomes:
        chromosomes = chromosomes.split("_")[0]
    ini_mapPos = int(oneSamLine2[3])
    mapPos = chromosomesCodingDic[chromosomes] + ini_mapPos  
    mapCigar = oneSamLine2[5]
    cigar_arr = []
    cigar_arr_one = ""
    for one in mapCigar:
        cigar_arr_one = cigar_arr_one + one
        if not is_number(one):
            cigar_arr.append(cigar_arr_one)
            cigar_arr_one = ""
    cigar_arr_first = cigar_arr[0]
    cigar_arr_last = cigar_arr[-1]
    if cigar_arr_first[-1] == "S" and int(cigar_arr_first[:-1]) >= 50:        
        this_end_value = mapPos - 1
        end_flag = 0
        for one_sv_end in sv_end_arr:
            if abs(this_end_value - one_sv_end) < 51:
                end_flag = 1
                break
        if end_flag == 0:
            sv_end_arr.append(this_end_value)
            read_len = len(oneSamLine2[9])
            if read_len >= 100:
                read_len_arr.append(read_len)
    if cigar_arr_last[-1] == "S" and int(cigar_arr_last[:-1]) >= 50:
        this_begin_value = mapPos + ref_span(cigar_arr)
        begin_flag = 0
        for one_sv_begin in sv_begin_arr:
            if abs(this_begin_value - one_sv_begin) < 51:
                begin_flag = 1
                break
        if begin_flag == 0:
            sv_begin_arr.append(this_begin_value)
            read_len = len(oneSamLine2[9])
            if read_len >= 100:
                read_len_arr.append(read_len)
sv_begin_arr = sorted(sv_begin_arr)
sv_end_arr = sorted(sv_end_arr)
this_samFile_arr2 = []
print "初步起止位置获取完成"

def same_sv(begin_pos, end_pos):
    threshold_value = 2000
    if end_pos > begin_pos and (end_pos - begin_pos) < threshold_value:
        return True
    else:
        return False

sv_result = []
for one_sv_begin in sv_begin_arr:
    for one_sv_end in sv_end_arr:
        if same_sv(one_sv_begin, one_sv_end):
            sv_result.append([one_sv_begin, one_sv_end])
sv_begin_arr = []
sv_end_arr = []
print "起止位置获取完成"


iniRepeatFileDir = "rmsk.txt"
iniRepeatObject = open(iniRepeatFileDir)
try:
     iniRepeatFile = iniRepeatObject.read( )
finally:
     iniRepeatObject.close( )
iniRepeatFile_rows = iniRepeatFile.split('\n')
iniRepeatFile_rows.pop()
repeat_arr = []
for one_iniRepeatFile_row in iniRepeatFile_rows:
    one_iniRepeatFile_row_arr = one_iniRepeatFile_row.split('\t')
    try:
        repeat_arr.append([chromosomesCodingDic[one_iniRepeatFile_row_arr[5]] + int(one_iniRepeatFile_row_arr[6]), chromosomesCodingDic[one_iniRepeatFile_row_arr[5]] + int(one_iniRepeatFile_row_arr[7])])
    except:
        continue
svInRepeat_account = 0
for one_sv in sv_result:
    for one_repeat in repeat_arr:
        if one_sv[0] >= one_repeat[0] and one_sv[0] <= one_repeat[1]:
            svInRepeat_account = svInRepeat_account + 1
            break
repeatPercent = float(svInRepeat_account) / float(len(sv_result))
repeat_arr = []


shortSV_account = 0
middleSV_account = 0
longSV_account = 0
for one_sv in sv_result:
    if (one_sv[1] - one_sv[0]) <= 200:
        shortSV_account = shortSV_account + 1
    elif (one_sv[1] - one_sv[0]) > 1000:
        longSV_account = longSV_account + 1
    else:
        middleSV_account = middleSV_account + 1
shortSV = float(shortSV_account) / float(len(sv_result))
middleSV = float(middleSV_account) / float(len(sv_result))
longSV = float(longSV_account) / float(len(sv_result))


readLen = float(sum(read_len_arr)) / float(len(read_len_arr))
gap_arr = []
for one_sv in sv_result:
    if one_sv == sv_result[0]:
        before_sv_begin = one_sv[0]
    else:
        now_sv_begin = one_sv[0]
        if str(now_sv_begin)[0:-9] == str(before_sv_begin)[0:-9]:      #同一个染色体号才算间隔，不同染色体不算间隔。
            gap_arr.append(now_sv_begin - before_sv_begin)
        before_sv_begin = now_sv_begin

smallGap_account = 0
smallGap_arr = []
for one_gap in gap_arr:
    if one_gap <= min(readLen, 20000):
        smallGap_account = smallGap_account + 1
        smallGap_arr.append(one_gap)
if len(smallGap_arr) == 0:
    RMB = 1.0
else:
    smallGap_ave = float(sum(smallGap_arr)) / float(len(smallGap_arr))
    RMB = float(readLen) / float(smallGap_ave)
HMDP = float(len(smallGap_arr)) / float(len(gap_arr))
readLen = int(readLen)

os.system("samtools view -bS tmp.sam > tmp.bam")
os.system("samtools sort tmp.bam > tmp_sort.bam")
os.system("samtools index tmp_sort.bam")
os.system("samtools depth tmp_sort.bam > tmp_depth.txt")
depthTxtObject = open("tmp_depth.txt")
try:
     depthTxtFile = depthTxtObject.read( )
finally:
     depthTxtObject.close( )
depthTxtFile_rows = depthTxtFile.split('\n')
depthTxtFile_rows.pop()
line_account = 0
line_sum = 0
for one_depthTxtFile_row in depthTxtFile_rows:
    line_sum = line_sum + int(one_depthTxtFile_row.split('\t')[2])
    line_account = line_account + 1
depth = float(line_sum) / float(line_account)
depth = int(round(depth))

print repeatPercent, shortSV, middleSV, longSV, RMB, HMDP, readLen, depth
os.system("rm tmp.sam tmp.bam tmp_sort.bam tmp_sort.bam.bai tmp_depth.txt")

metaFeature = [[repeatPercent, shortSV, middleSV, longSV, RMB, HMDP, readLen, depth]]
precision_clf = joblib.load("precision_metaTarget_model.m")
recall_clf = joblib.load("recall_metaTarget_model.m")
F1_clf = joblib.load("F1_metaTarget_model.m")
print "the highest precision value software:", precision_clf.predict(metaFeature)[0]
print "the highest recall value software:", recall_clf.predict(metaFeature)[0]
print "the highest F1 value software:", F1_clf.predict(metaFeature)[0]

