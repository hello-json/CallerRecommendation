# -*- coding: UTF-8 -*-
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--the_input', help='the input batch samples dir, eg: /mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles', required=True, type=str)
parser.add_argument('-o', '--the_output', help='the output recorded f1score file, eg: /mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/recorededF1scoreFile.tsv', required=True, type=str)
args = parser.parse_args()
batchSamlesDir = args.the_input
recorededF1scoreFileName = args.the_output

#batchSamlesDir = "/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles"

faFeature_arr = ["l_hr_hd", "l_hr_nd", "l_nr_hd", "l_nr_nd", "m_hr_hd", "m_hr_nd", "m_nr_hd", "m_nr_nd", "s_hr_hd", "s_hr_nd", "s_nr_hd", "s_nr_nd"]
readLen_arr = ["1000", "2000", "3000", "5000", "10000", "15000", "20000", "25000"]
depth_arr = ["10", "30", "50", "70", "90", "110", "130", "150"]
software_set_arr = [["nanosv"], ["picky"], ["sniffles"], ["pbsv"], ["cutesv"], ["nanosv", "picky"], ["nanosv", "sniffles"], ["nanosv", "pbsv"], ["nanosv", "cutesv"], ["picky", "sniffles"], ["picky", "pbsv"], ["picky", "cutesv"], ["sniffles", "pbsv"], ["sniffles", "cutesv"], ["pbsv", "cutesv"], ["nanosv", "picky", "sniffles"], ["nanosv", "picky", "pbsv"], ["nanosv", "picky", "cutesv"], ["nanosv", "sniffles", "pbsv"], ["nanosv", "sniffles", "cutesv"], ["nanosv", "pbsv", "cutesv"], ["picky", "sniffles", "pbsv"], ["picky", "sniffles", "cutesv"], ["picky", "pbsv", "cutesv"], ["sniffles", "pbsv", "cutesv"], ["nanosv", "picky", "sniffles", "pbsv"], ["nanosv", "picky", "sniffles", "cutesv"], ["nanosv", "picky", "pbsv", "cutesv"], ["nanosv", "sniffles", "pbsv", "cutesv"], ["picky", "sniffles", "pbsv", "cutesv"], ["nanosv", "picky", "sniffles", "pbsv", "cutesv"]]
#software_arr = ["nanosv", "picky", "sniffles", "pbsv", "cutesv"]

faFeature_dic = {}
FaFeatureFileDir = batchSamlesDir + "/faInfo.tsv"
FaFeatureObject = open(FaFeatureFileDir)
try:
     FaFeatureFile = FaFeatureObject.read( )
finally:
     FaFeatureObject.close( )
FaFeatureFile_rows = FaFeatureFile.split('\n')
FaFeatureFile_rows.pop()
for FaFeatureFile_row in FaFeatureFile_rows:
    FaFeatureFile_row_arr = FaFeatureFile_row.split("\t")
    repeat_percent = FaFeatureFile_row_arr[1]
    short_percent = FaFeatureFile_row_arr[2]
    middle_percent = FaFeatureFile_row_arr[3]
    long_percent = FaFeatureFile_row_arr[4]
    faFeature_dic[FaFeatureFile_row_arr[0]] = [repeat_percent, short_percent, middle_percent, long_percent]
#print faFeature_dic

#将vcf文件变成数组的函数开始
def getPredictionArr(vcfFile):
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
    return prediction
#将vcf文件变成数组的函数结束

#将答案文件变成数组的函数开始
def getAnswerArr(standerFile):
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
    return answer
#将答案文件变成数组的函数结束

#将vcf文件数组和答案文件数组合并并去重的函数开始
def getAnswerPlusPredictionArr(prediction, answer):
    answerExceptPrediction = []
    for one_prediction in prediction:
        theFlag = 0
        for one_answer in answer:
            if ifSame(one_prediction, one_answer):
                theFlag = 1
                break
        if theFlag == 0:
            answerExceptPrediction.append(one_prediction)
    answerPlusPrediction = answer + answerExceptPrediction
    return answerPlusPrediction
#将vcf文件数组和答案文件数组合并并去重的函数结束

#判断约等函数开始
def ifSame(site1, site2):
    theSubtractThreshold = 10
    if abs(int(site1) - int(site2)) < theSubtractThreshold:
        return True
    else:
        return False
#判断约等函数结束

#评价指标计算函数开始(注意：1、结构变异检测这种情况TN值恒为0，因为答案并不会给出真阴性的值，给出的就是真阳性即样本里发生的变异。2、发生异常时即分母为0的时候，分子必为0。这个可以从混淆矩阵各指标的计算公式中看出来，除非分母中有一个值为负数，然而这是不可能的。3、在现在这种情况下，只有precision值可能出现异常，因为有可能有某个软件一个变异也没有检出来，此时precision值的分母为TP+FP=0。而混淆矩阵的其他值在计算时候，虽然分子是0，但分母由于FN不为0使得分母不为0，式子可以正常计算)
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
    return TP, FP, TN, FN, Accuracy, Precision, Recall, F_measure
#评价指标计算函数结束

#计算读段变异负荷和高变异区占比函数开始
def getRMBandHMDP(readLen, answerArr):
    mutation_distance_arr = []
    theOneAnswer = int(answerArr[0])
    for nowOneAnswer in answerArr:
        if int(nowOneAnswer) == int(theOneAnswer):
            continue
        else:
            mutation_distance_arr.append(int(nowOneAnswer) - int(theOneAnswer))
            theOneAnswer = int(nowOneAnswer)
    smallerThanReadLenSum = 0           #统计小于读长的变异间距数目
    all_smallerThanReadLenLength = 0           #计算小于读长的变异间距长度之和，用于后面求均值
    for one_mutation_distance in mutation_distance_arr:
        if one_mutation_distance < min(int(readLen), 20000):         #因为当读长大于20000时，会有很多长间距混进来，干扰均值计算。
            all_smallerThanReadLenLength = all_smallerThanReadLenLength + one_mutation_distance
            smallerThanReadLenSum = smallerThanReadLenSum + 1
    if smallerThanReadLenSum == 0:             #当没有间距小于读长时，直接定义RMB值为1
        RMB = "1"
    else:                             #当有间距小于读长时，计算间距平均值，并用读长除以间距平均值
        ave_smallerThanReadLenLength = int(float(all_smallerThanReadLenLength) / float(smallerThanReadLenSum))
        RMB = str(float(readLen) / float(ave_smallerThanReadLenLength))
    highMutationDensePercent= str(float(smallerThanReadLenSum) / float(len(mutation_distance_arr)))
    return RMB, highMutationDensePercent
#计算读段变异负荷和高变异区占比函数结束

resultFile = open(recorededF1scoreFileName, 'w')
for one_faFeature in faFeature_arr:
    print one_faFeature
    standerFile = batchSamlesDir + "/" + one_faFeature + "/" + one_faFeature + ".answer"
    answerArr = getAnswerArr(standerFile)
    for one_readLen in readLen_arr:
        RMB, highMutationDensePercent = getRMBandHMDP(one_readLen, answerArr)
        for one_depth in depth_arr:
            software_set_arr_recall_str = ""
            for one_software_set in software_set_arr:
                ini_arr = []
                for one_software in one_software_set:                    
                    vcfFile = batchSamlesDir + "/" + one_faFeature + "/testAlterDepth_" + one_readLen + "readLen/" + one_depth + "/" + one_software + "/" + one_software + ".vcf"
                    thisSoftware_predictionArr = getPredictionArr(vcfFile)
                    now_software_set_predictionArr = getAnswerPlusPredictionArr(thisSoftware_predictionArr, ini_arr)  #getAnswerPlusPredictionArr函数本来是用来将软件结果数组和答案数组进行合并的，这里正好用来合并两个软件的结果
                    ini_arr = now_software_set_predictionArr[:]
                answerPlusPredictionArr = getAnswerPlusPredictionArr(now_software_set_predictionArr, answerArr)
                tp, fp, tn, fn, accuracy, precision, recall, f_measure = caculate(answerArr, now_software_set_predictionArr, answerPlusPredictionArr)
                #software_set_arr_recall_str = software_set_arr_recall_str + str(recall) + "\t"      #生成tsv文件
                software_set_arr_recall_str = software_set_arr_recall_str + str(recall) + ","      #生成csv文件
            software_set_arr_recall_str_noLastT = software_set_arr_recall_str[:-1]
            #resultFile_row = faFeature_dic[one_faFeature][0] + "\t" + faFeature_dic[one_faFeature][1] + "\t" + faFeature_dic[one_faFeature][2] + "\t" + faFeature_dic[one_faFeature][3] + "\t" + RMB + "\t" + highMutationDensePercent + "\t" + one_readLen + "\t" + one_depth + "\t" + software_set_arr_recall_str_noLastT + "\n"      #生成tsv文件
            resultFile_row = faFeature_dic[one_faFeature][0] + "," + faFeature_dic[one_faFeature][1] + "," + faFeature_dic[one_faFeature][2] + "," + faFeature_dic[one_faFeature][3] + "," + RMB + "," + highMutationDensePercent + "," + one_readLen + "," + one_depth + "," + software_set_arr_recall_str_noLastT + "\n"      #生成csv文件
            resultFile.write(resultFile_row)
resultFile.close()
