import os
import sys
import csv
import itertools 
import socket
import ipaddress
import pandas as pandasForSortingCSV
import pandas as pd
from datetime import datetime

#write file count to csv file
def  write_to_file(consolidate_list):
    print("creating final file")
    now = datetime.now().time() # time object

    print("now =", now)
    file = open('Token_Ouput.csv', 'w', newline ='')
    with file:    
       write = csv.writer(file)
       write.writerow(['ColA','ColB','ColC','ColD','ColE','ColF','ColG','ColH'])
       write.writerows(consolidate_list)
    # assign dataset
    csvData = pandasForSortingCSV.read_csv("Token_Ouput.csv")
    print("\Before sorting:")
    now = datetime.now().time() # time object

    print("now =", now)
   # print(csvData)                                    
# displaying unsorted data frame
   
  
# sort data frame
    csvData.sort_values(csvData.columns[0], 
                       axis=0,
                       ascending=True, 
                       inplace=True)
    #print("\After sorting:")
    #print(csvData)
    df = pd.read_csv("Token_Ouput.csv")
    #print (df.columns[0])
    sorted_df = df.sort_values(by=["ColA"], axis=0, ascending=False)
    sorted_df.to_csv('homes_sorted.csv', index=False, header=None)

def check_valid_address(address):
   
    try:
        ip = ipaddress.ip_address(address)

        if isinstance(ip, ipaddress.IPv4Address):
            return("valid")
        elif isinstance(ip, ipaddress.IPv6Address):
            return("valid")
    except ValueError:
        return("invalid")

# function to get unique values
def unique_list(count_list, token_list, token_count):
 
    # initialize a null list
    unique_list_count = []
    unique_list_token = []
    index= 0;
    item_index =0
    composed_list = []
    
    #this loop is to retrieve the token array based on token count
   #this loop is to retrieve the token array based on token count
    for i, list_item in enumerate(token_list):
      composed_list.append(token_list[i][0:token_count])
    print("composed list created")
    now = datetime.now().time() # time object
    print("now =", now)
    consolidate_list =[]
    #conslidate_list = count_list + composed_list
    list_index=0
    df3=pd.DataFrame(count_list)
    df4=pd.DataFrame(composed_list)
    df5=pd.concat([df3, df4])
    df = df3.merge(df4, how="inner", left_index=True, right_index=True)
    print(df)
   # for i in  range(0,len(composed_list)-1):
    #    consolidate_list[i] =  composed_list[i]
     #   consolidate_list.insert(0,int(count_list[i]))
  #  for x in composed_list:
   #     item_index = composed_list.index(x)
        
    #    consolidate_list.append(composed_list[item_index])
     #   consolidate_list[list_index].insert(0,count_list[item_index])
      #  list_index +=1
       # print(list_index)
    print("consolidated list created")
    now = datetime.now().time() # time object
    print("now =", now)
    print("aggregation in progress")
    #df= pd.DataFrame(consolidate_list)

    #print(df)
    column_count = df.shape[1]
    columns= []
    
    tokenheader =[]
    
    for i in range(0,column_count-1):
        tokenheader.append("Token_"+ str(i))
    
    columns = list(tokenheader)
    columns.insert(0,'Aggr')
    df.columns = columns
    #df.columns = ['Aggr', 'Token1', 'Token2', 'Token3']
    df.fillna(0, inplace=True)
    #df2 = df.groupby(['Token1', 'Token2', 'Token3'], as_index=False).agg({"Aggr":"sum"})
    #df.to_csv('before_token.csv', index=False, header=True)
    #df6 = df.groupby(tokenheader).size().reset_index(name='counts')
    #df6.to_csv('before_token.csv', index=False, header=True)
    df2 = df.groupby(tokenheader, as_index=False).agg({"Aggr":"sum"})
    df2 = df2.drop_duplicates(subset=tokenheader)
    df2.reset_index(drop=True)
    #print(df2)
    cols = df2.columns.tolist()
    cols.insert(0, cols.pop(cols.index('Aggr')))
    df2 = df2.reindex(columns= cols)
    #print(df2)
    print("now =", now)
    print("before sorting")
    sorted_df = df2.sort_values(by=["Aggr"], axis=0, ascending=False)
    sorted_df.to_csv('homes_sorted.csv', index=False, header=None)
    exit(0)
    ### this could be end
    
    # traverse for all elements
    item_count = 0
    #for (x,y) in zip(composed_list,count_list):
    for x in composed_list:
        # check if exists in unique_list or not
        #item_index = unique_list_token.index(x)
        if x not in unique_list_token:
            unique_list_token.append(x)
            unique_list_count.append(count_list[item_count])
        else:
           item_index = unique_list_token.index(x)
           unique_list_count[item_index] = int(unique_list_count[item_index]) + int(count_list[item_count])#int(y)
        
        print(item_count,"Actual", len(composed_list),len(count_list) )
        print(len(unique_list_token), len(unique_list_count))
        item_count+=1
    # print list
    consolidate_list =[]
    list_index=0
    now = datetime.now().time() # time object
    print("now =", now)
    print("before consolidating")
    for x in unique_list_token:
        item_index = unique_list_token.index(x)
        
        consolidate_list.append(unique_list_token[item_index])
        consolidate_list[list_index].insert(0,unique_list_count[item_index])
        list_index +=1
    print("after consolidating")
    now = datetime.now().time() # time object

    print("now =", now)
    write_to_file(consolidate_list)
    

with open('combined_csv_1643302830.csv', newline='') as csvfile:
    
  

   
  #  csv_reader = csv.DictReader(csvfile)
    df = pd.read_csv('combined_csv_1643302830.csv')
    print("Rows:",df.shape[0],"Columns:",df.shape[1])
    now = datetime.now().time() # time object

    print("now =", now)
    print("Reading files, please wait...")
    #print(df)
    df=df.dropna(axis=0, how='all')
    df.columns = df.columns.str.replace(' ', '')
  #  df.to_csv('reference.csv', index=False, header=None)
    #print(df)
    #print("New Rows:",df.shape[0],"New Columns:",df.shape[1])
    count_list = []
    token_list = []
    token_split_list = []
    #for row in csv_reader:
    #for (idx, row) in df.itertuples():
    item_number=0
    for  row in df.itertuples():
        #print(row.IPAddr)
        #print(row[df.columns.get_loc(' IP_Addr')])
        #print(row.index)
        #print(row.loc[' Name Field_1'])
        #if(pd.isnull(row[' Name Field_1'])):
         #   print('true')
        # row variable is a list that represents a row in csv
        #if((row.loc[' Name Field_1']) != ""):
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
    
    print("now =", now)
    unique_list(count_list,token_list,2)
    #print(count_list)
    #print(token_list)