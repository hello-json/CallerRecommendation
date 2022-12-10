# -*- coding: UTF-8 -*-
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--the_vcf', help='the vcf Result of SV software', required=True, type=str)
parser.add_argument('-a', '--the_stander', help='the standard Answer', required=True, type=str)  #stander单词应该是standard，将错就错了。不过其实stander本身也有标准的意思，是名词。
args = parser.parse_args()
vcfFile = args.the_vcf
standerFile = args.the_stander

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
            prediction.append(int(vcf_file_row.split('\t')[1]))
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
    try:
        answer.append(int(stander_file_row.split('\t')[0]))
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

#评价指标计算函数开始(注意：出现异常即分母为0的时候，分子必为0。这个可以从混淆矩阵各指标的计算公式中看出分母中都有一个加项是分子，所以除非分母中有一个值为负数。然而这是不可能的，因为TP、FP、TN、FN的值肯定都是大于0的。所以，我把下面函数的except情况都直接赋值为0了！！！！！！)
def caculate(answer, prediction, answerPlusPrediction):
    answerPlusPrediction_length = len(answerPlusPrediction)
    answerFlagArr = [0 for x in range(answerPlusPrediction_length)]
    predictionFlagArr = [0 for y in range(answerPlusPrediction_length)]
    i = -1
    for answerPlusPrediction_element in answerPlusPrediction:
        i = i + 1
        for answer_element in answer:
            if ifSame(answer_element, answerPlusPrediction_element):
                answerFlagArr[i] = 1
                break
        for prediction_element in prediction:
            if ifSame(prediction_element, answerPlusPrediction_element):
                predictionFlagArr[i] = 1
                break
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for j in range(answerPlusPrediction_length):
        if answerFlagArr[j] == 1 and predictionFlagArr[j] == 1:
            TP = TP + 1
        if answerFlagArr[j] == 0 and predictionFlagArr[j] == 1:
            FP = FP + 1  
        if answerFlagArr[j] == 0 and predictionFlagArr[j] == 0:
            TN = TN + 1 
        if answerFlagArr[j] == 1 and predictionFlagArr[j] == 0:
            FN = FN + 1
    try:
        Accuracy = float(TP + TN) / float(TP + FP + TN + FN)
    except:
        #Accuracy = str(float(TP + TN)) + " / " + str(float(TP + FP + TN + FN))
        Accuracy = 0
    try:
        Precision = float(TP) / float(TP + FP)
    except:
        #Precision = str(float(TP)) + " / " + str(float(TP + FP))
        Precision = 0
    try:
        Recall = float(TP) / float(TP + FN)
    except:
        #Recall = str(float(TP)) + " / " + str(float(TP + FN))
        Recall = 0
    try:
        F_measure = float(2 * TP) / float(2 * TP + FN + FP)
    except:
        #F_measure = str(float(2 * TP)) + " / " + str(float(2 * TP + FN + FP))
        F_measure = 0
    
    print "TP:" + str(TP)
    print "FP:" + str(FP)
    print "TN:" + str(TN)
    print "FN:" + str(FN)
    print "Accuracy:" + str(Accuracy)
    print "Precision:" + str(Precision)
    print "Recall:" + str(Recall)
    print "F_measure:" + str(F_measure)
    
    #return str(TP), str(FP), str(TN), str(FN), str(Accuracy), str(Precision), str(Recall), str(F_measure), str(Accuracy2), str(Precision2), str(Recall2), str(F_measure2)
#评价指标计算函数结束

'''
#测试用开始
answer = [20, 80, 140, 200]
prediction = [20, 80, 260, 300]
#测试用结束
'''

answerPlusPrediction = []
for one_prediction in prediction:
    theFlag = 0
    for one_answer in answer:
        if ifSame(one_prediction, one_answer):
            theFlag = 1
            break
    if theFlag == 0:
        answerPlusPrediction.append(one_prediction)
answerPlusPrediction = answer + answerPlusPrediction
caculate(answer, prediction, answerPlusPrediction)
