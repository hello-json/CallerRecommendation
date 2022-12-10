# -*- coding: UTF-8 -*
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--i_sam', help='the input sam', required=True, type=str)
parser.add_argument('-o', '--o_sam', help='the output sam', required=True, type=str)
args = parser.parse_args()
input_sam = args.i_sam
output_sam = args.o_sam

samFileDir = input_sam
samObject = open(samFileDir)
try:
     samFile = samObject.read( )
finally:
     samObject.close( )
samFile_rows = samFile.split('\n')
samFile_rows.pop()

newSamFile = open(output_sam, 'w')
for oneRow in samFile_rows:
    if oneRow.startswith("@"):
        newSamFile.write(oneRow + "\n")
    else:
        oneRow_arr = oneRow.split("\t")
        if not oneRow_arr[4].startswith("-"):
            newSamFile.write(oneRow + "\n")
    
newSamFile.close()

