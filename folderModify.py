import os,sys
import shutil

currentline=[]
directoryName = "C:\\Users\\sramadas\\source\\repos\\folderModify\\abc"
with open("list.txt", "r") as filestream:
    for line in filestream:
            currentline = line.split(",")
            for count, currentline[0] in enumerate(os.listdir(directoryName)):
              # os.chdir("C:\\Users\\sramadas\\source\\repos\\folderModify\\abc")
               src = directoryName +"\\"+currentline[0]
               dst = directoryName +"\\"+currentline[1]
               os.rename(src,dst)