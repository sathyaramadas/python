import os
import sys
import csv
import itertools 
import os
import glob
import time
import sys
import subprocess
import pandas as pd
from datetime import datetime
from csv import reader

#write file count to csv file
def  write_to_file(consolidate_list):
    os.chdir(source_path)
 #   print(source_path)
    file = open("token_update_unsorted.csv", 'w')
    with file:    
       write = csv.writer(file)
       write.writerow(['ColA','ColB','ColC','ColD','ColE','ColF','ColG','ColH'])
       write.writerows(consolidate_list)
 
#sort the CSV    
    df = pd.read_csv("token_update_unsorted.csv")
    sorted_df = df.sort_values(by=['ColA'], ascending=False)
    sorted_df.to_csv(output_file_name, index=False, header=None)       

# function to get unique values
def unique_list(count_list, token_list, token_count):
 
    # initialize a null list
    unique_list_count = []
    unique_list_token = []
    index= 0;
    item_index =0
    composed_list = []

    #this loop is to retrieve the token array based on token count
    for i, list_item in enumerate(token_list):
      composed_list.append(token_list[i][0:token_count])
    print("composed list created")
    now = datetime.now().time() # time object
    print("token seperation completed")
    # traverse for all elements
    #conslidate_list = count_list + composed_list
    list_index=0
    df3=pd.DataFrame(count_list)
    df4=pd.DataFrame(composed_list)
    df5=pd.concat([df3, df4])
    df = df3.merge(df4, how="inner", left_index=True, right_index=True)
    print("consolidated list created")
    now = datetime.now().time() # time object
    print("now =", now)
    print("aggregation in progress")
    #df= pd.DataFrame(consolidate_list)
    column_count = df.shape[1]
    columns= []
    
    tokenheader =[]
    
    for i in range(0,column_count-1):
        tokenheader.append("Token_"+ str(i))
    
    columns = list(tokenheader)
    columns.insert(0,'Aggr')
    df.columns = columns
 
    df.fillna(0, inplace=True)
 
   
    df2 = df.groupby(tokenheader, as_index=False).agg({"Aggr":"sum"})
    df2 = df2.drop_duplicates(subset=tokenheader)
    df2.reset_index(drop=True)
    
    cols = df2.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Aggr')))
    df2 = df2.reindex(columns= cols)
    now = datetime.now().time() # time object
    print("now =", now)
    sorted_df = df2.sort_values(by=["Aggr"], axis=0, ascending=False)
    os.chdir(source_path)
    sorted_df.to_csv(output_file_name, index=False, header=None)
    exit(0)
    

def readCSVFile(fileName,tokencount):
    #with open(fileName) as csvfile:
    df = pd.read_csv(fileName)
    print("Rows:",df.shape[0],"Columns:",df.shape[1])
    now = datetime.now().time() # time object

    print("now =", now)
    print("Reading files, please wait...")
    #print(df)
    df=df.dropna(axis=0, how='all')
    df.columns = df.columns.str.replace(' ', '')
    #print(df)
    #print("New Rows:",df.shape[0],"New Columns:",df.shape[1])
    count_list = []
    token_list = []
    token_split_list = []
    item_number=0
    for  row in df.itertuples():
       
        if(pd.isnull(row.NameField_1)  or row.NameField_1 == ' '):
            token_split_list = (row.IPAddr).split(';')
        
        elif(row.NameField_1 == row.IPAddr):
            token_split_list = (row.IPAddr).split(';')
        else:
            token_split_list = (row.RevField_1).split('.')
        #print(token_split_list, len(token_split_list))
        token_list.append(token_split_list)
        count_list.append(row.OctetsAggr)
        item_number +=1
        #print(item_number)

    print("exiting field creation")
    consolidate_list =[]
    now = datetime.now().time() # time object
    
    print("Field creation completed")
    print("now=", now)
    unique_list(count_list,token_list,2)

     

def main():
    cwd = os.getcwd()
    global dest_path
    global epoch_time
    global source_path
    global output_file_name
    fileList =[]
    n = len(sys.argv)
    if(n < 4):
      exit("usage : <script.py> tokencount <inputfolderpath> <outputfilename>")
      exit
    #fileList = []
    tokencount = sys.argv[1]
    source_path = sys.argv[2]
    output_file_name = sys.argv[3]
    if(n==5):
      fileList = sys.argv[4].split(",")
      
    if os.name == 'nt':
        source_dir = cwd + "\\" + "Source"
        dest_path = source_path + "\\" + "output"
    else:
        source_dir = cwd + "/" + "Source"
        dest_path = source_path + "/" + "output"
    os.chdir(source_path)
   # dest_directory = "//output"
    #dest_path = source_path + "\\" + "output"
    if not os.path.exists(dest_path):
      os.mkdir(dest_path)
    extension = 'csv'
    bin_extension = 'app_disc'
    epoch_time = int(time.time())
    output_file = "combined_csv_" + str(epoch_time) + ".csv"

    all_bin_filenames = [i for i in glob.glob('*.{}'.format(bin_extension))]
    if (len(fileList) >= 1):
       all_bin_filenames = fileList

    for f in all_bin_filenames:
        system_command = "./asi2csv" + " -o " + dest_path + " " + f 
        os.system(system_command)
    
    os.chdir(dest_path)
    #all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    all_filenames = [i for i in glob.glob('*app_disc.{}'.format(extension))]
   
    if (len(fileList) >= 1):
       all_filenames = fileList
    
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    os.chdir(dest_path)
    combined_csv.to_csv( output_file, index=False,header=True, encoding='utf-8-sig')
    readCSVFile(output_file,tokencount)

if __name__ == "__main__":
    main()
