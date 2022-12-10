# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold
import numpy as np
import random

markedFileDir = "/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles/markedResult/markedLableFile.csv"
markedFileObject = open(markedFileDir)
try:
     markedFile = markedFileObject.read( )
finally:
     markedFileObject.close( )
markedFile_rows = markedFile.split('\n')
markedFile_rows.pop()
feature_arr = []
label_arr = []
for one_markedFile_row in markedFile_rows:
    one_markedFile_row_arr = one_markedFile_row.split(",")
    feature_arr.append([float(one_markedFile_row_arr[0]), float(one_markedFile_row_arr[1]), float(one_markedFile_row_arr[2]), float(one_markedFile_row_arr[3]), float(one_markedFile_row_arr[4]), float(one_markedFile_row_arr[5]), float(one_markedFile_row_arr[6]), float(one_markedFile_row_arr[7])])
    label_arr.append(one_markedFile_row_arr[-1].strip('\r'))    #F1最大为标签(末尾有个换行符，虽然不去掉也行，但还是去了吧)
    #label_arr.append(one_markedFile_row_arr[-3])        #precision最大为标签
    #label_arr.append(one_markedFile_row_arr[-2])        #recall最大为标签
    
recordedFileDir = "/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles/markedResult/recorededF1scoreFile.csv"      #F1
#recordedFileDir = "/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles/markedResult/recorededPrecisionFile.csv"     #precision
#recordedFileDir = "/mnt/X500/farmers/wangshj/doctoralPeriod/thirdPoint/simData/makeABatchOfSamles/markedResult/recorededRecallFile.csv"      #recall
recordedFileObject = open(recordedFileDir)
try:
     recordedFile = recordedFileObject.read( )
finally:
     recordedFileObject.close( )
recordedFile_rows = recordedFile.split('\n')
recordedFile_rows.pop()
recordedValue_arr = []
for one_recordedFile_row in recordedFile_rows:
    one_recordedFile_row_arr = one_recordedFile_row.split(",")
    recordedValue_arr.append({"nanosv": float(one_recordedFile_row_arr[8]), "picky": float(one_recordedFile_row_arr[9]), "sniffles": float(one_recordedFile_row_arr[10]), "pbsv": float(one_recordedFile_row_arr[11]), "cutesv": float(one_recordedFile_row_arr[12])})

#使用十折交叉验证推荐的RA值开始（注意这个交叉验证包只能用numpy数组）
kf = KFold(768, shuffle=True)          #把折数设置成数据个数就是留一法了，注意在分每一类计算RA值的这个脚本里面，只能设置折数为数据个数，不然没法算。
feature_arr = np.array(feature_arr)
label_arr = np.array(label_arr)
all_RA = []
all_nanosv_RA = []
all_picky_RA = []
all_sniffles_RA = []
all_pbsv_RA = []
all_cutesv_RA = []
for train_idx, test_idx in kf.split(feature_arr, label_arr):
    #print(train_idx)
    #print(len(train_idx))
    X_train, y_train = feature_arr[train_idx], label_arr[train_idx]
    X_test, y_test = feature_arr[test_idx], label_arr[test_idx]
    #clf = RandomForestClassifier(n_estimators=100)
    clf = RandomForestClassifier(n_estimators=70, max_depth=7, min_samples_split=2, min_samples_leaf=1, max_features=5, oob_score=False, random_state=10)      #F1score lable use
    #clf = RandomForestClassifier(n_estimators=90, max_depth=13, min_samples_split=22, min_samples_leaf=1, max_features=5, oob_score=False, random_state=10)      #precision lable use
    #clf = RandomForestClassifier(n_estimators=100, max_depth=7, min_samples_split=2, min_samples_leaf=1, max_features=1, oob_score=False, random_state=10)      #recall lable use
    clf.fit(X_train, y_train) 
    y_pred = clf.predict(X_test)

    RA_arr = []
    j = -1              #这里的j就是用来按顺序依次输出y_pred
    for one_index in test_idx:
        j = j + 1
        now_recordedValue_dic = recordedValue_arr[one_index]
        worst_value = min(now_recordedValue_dic.values())
        best_value = max(now_recordedValue_dic.values())
        recommend_value = now_recordedValue_dic[y_pred[j]]
        RA = (recommend_value - worst_value) / (best_value - worst_value)
        RA_arr.append(RA)
    RA_average = sum(RA_arr)/len(RA_arr)
    if y_test[0] == "nanosv":
        all_nanosv_RA.append(RA_average)
    if y_test[0] == "picky":
        all_picky_RA.append(RA_average)
    if y_test[0] == "sniffles":
        all_sniffles_RA.append(RA_average)
    if y_test[0] == "pbsv":
        all_pbsv_RA.append(RA_average)
    if y_test[0] == "cutesv":
        all_cutesv_RA.append(RA_average)
    all_RA.append(RA_average)
recommend_RA_value = sum(all_RA)/len(all_RA)
recommend_nanosv_RA_value = sum(all_nanosv_RA)/len(all_nanosv_RA)
recommend_picky_RA_value = sum(all_picky_RA)/len(all_picky_RA)
recommend_sniffles_RA_value = sum(all_sniffles_RA)/len(all_sniffles_RA)
recommend_pbsv_RA_value = sum(all_pbsv_RA)/len(all_pbsv_RA)
recommend_cutesv_RA_value = sum(all_cutesv_RA)/len(all_cutesv_RA)
print "recommend_overall :", recommend_RA_value
print "recommend_nanosv :", recommend_nanosv_RA_value
print "recommend_picky :", recommend_picky_RA_value
print "recommend_sniffles :", recommend_sniffles_RA_value
print "recommend_pbsv :", recommend_pbsv_RA_value
print "recommend_cutesv :", recommend_cutesv_RA_value
#使用十折交叉验证推荐的RA值结束(注意：这里面将feature_arr和label_arr转成了numpy数组，如果不屏蔽这部分的情况下运行下面代码出错时记得考虑这个！！！！！！)


#验证fixed的RA值开始
fixed_arr = ["nanosv", "picky", "sniffles", "pbsv", "cutesv"]
for one_fixed in fixed_arr:
    fixed_RA_arr = []
    for fixed_recordedValue_index in range(len(recordedValue_arr)):
        fixed_recordedValue_dic = recordedValue_arr[fixed_recordedValue_index]
        fixed_worst_value = min(fixed_recordedValue_dic.values())
        fixed_best_value = max(fixed_recordedValue_dic.values())
        fixed_value = fixed_recordedValue_dic[one_fixed]
        fixed_RA = (fixed_value - fixed_worst_value) / (fixed_best_value - fixed_worst_value)
        fixed_RA_arr.append(fixed_RA)
    fixed_RA_average = sum(fixed_RA_arr)/len(fixed_RA_arr)
    print one_fixed, ":", fixed_RA_average
#验证fixed的RA值结束


#验证random的RA值开始
random_arr = ["nanosv", "picky", "sniffles", "pbsv", "cutesv"]
random_RA_arr = []
for random_recordedValue_index in range(len(recordedValue_arr)):
    random_recordedValue_dic = recordedValue_arr[random_recordedValue_index]
    random_worst_value = min(random_recordedValue_dic.values())
    random_best_value = max(random_recordedValue_dic.values())
    random_value = random_recordedValue_dic[random.choice(random_arr)]
    random_RA = (random_value - random_worst_value) / (random_best_value - random_worst_value)
    random_RA_arr.append(random_RA)
random_RA_average = sum(random_RA_arr)/len(random_RA_arr)
print "random :", random_RA_average
#验证random的RA值结束
