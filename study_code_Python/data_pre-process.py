# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:39:51 2023

@author: Yimeng Liu
"""
import numpy as np
import pandas as pd
import re


df1 = pd.read_excel('OTU table.xlsx')
microsname=list(df1['Taxonomy'])#microbiome name list
microclass=list(df1['Tax_detail'])#microbiome name class
microindex=list(range(0,len(df1),1))
microsname_cut=list(df1['Taxonomy'])#the name of microbiome with suitable abundance
microclass_cut=list(df1['Tax_detail'])#the class of microbiome with suitable abundance
microindex_cut=list(range(0,len(df1),1))
df=df1.drop(['Taxonomy'],axis=1)
df=df.drop(['Tax_detail'],axis=1)

peoplename=list(df.columns.values.tolist())#name of patients
df.columns=list(range(1,(df.columns.size+1),1))
###############1. Convert the OTU data to integers##################
integer={}
integer_all=[]
for i in range(1,df.columns.size+1,1):
    each=list(df[i])
    each_int=[]
    for j in range(0,len(df),1):
        each_int.append(round(each[j]/df[1][41]))
        integer_all.append(round(each[j]/df[1][41]))
    integer[i]=each_int
df_integer=pd.DataFrame.from_dict(integer)

###############2. delete microbiome with all 0 abundance################
df=df.drop(labels=len(df)-1, axis=0)
df_integer=df_integer.drop(labels=len(df), axis=0)
microclass_cut.remove(microclass[len(df)])
microsname_cut.remove(microsname[len(df)])
microindex_cut.remove(microindex[len(df)])
for i in range(len(df)-1,-1,-1):
    if sum(list(df.iloc[i]))==0:
        df=df.drop(labels=(i), axis=0)
        microclass_cut.remove(microclass[i])
        microsname_cut.remove(microsname[i])
        microindex_cut.remove(microindex[i])
for i in range(len(df_integer)-1,-1,-1):
    if sum(list(df_integer.iloc[i]))==0:
        df_integer=df_integer.drop(labels=(i), axis=0)        
#######3. Change the abundance that is too small to 0 to open up the gap between microbes##################
'threshold is 10'
threshold=10
for i in range(0,len(df_integer),1):
    count=0
    for j in range(1,df_integer.columns.size+1,1):        
        if df_integer[j][i]<threshold:
            df_integer[j][i]=0
            df[j][i]=0
        else:
            continue
###############4. delete microbiome with expression rate lower than 10%#################
specice_express=[]
for i in df.index:
    count=0
    for j in range(1,df.columns.size+1,1):        
        if df[j][i]!=0:
            count=count+1
        else:
            continue
    specice_express.append(count/df.columns.size)
specice_express_sort=sorted(specice_express,reverse=True)
specice_express_index=sorted(range(len(specice_express)), key=lambda k: specice_express[k],reverse=True)#排序，内容和spearman的差不多

threshold_rate=0.1
delete_10=[]
for i in range(0,len(specice_express),1):
    if specice_express[i] < threshold_rate:
        delete_10.append(i)
df=df.drop(labels=delete_10, axis=0)
df_integer=df_integer.drop(labels=delete_10, axis=0)

microclass_delete=[]
microsname_delete=[]
for i in delete_10:
    microclass_delete.append(microclass_cut[i])
    microsname_delete.append(microsname_cut[i])
    microindex_cut.remove(i)
for i in microclass_delete:
    microclass_cut.remove(i)
for i in microsname_delete:
    microsname_cut.remove(i)
    
########5. For microbiomes that remained, normal abundance values are restored##
df_new={}
for i in microindex_cut:
    df_new[i]=list(df1.iloc[i])
df_new=pd.DataFrame.from_dict(df_new)
df_array=df_new.stack()#列转行
df_new=df_array.unstack(0)#在行转列，完成dataframe转置 
df_new=df_new.drop(labels=[0,119],axis=1)

df=df_new
#####################6. nomalization all dataset#############################
species_left=df.index
df.index=pd.Series(range(0,len(df),1))
df_integer.index=pd.Series(range(0,len(df_integer),1))
df_nor={}
for i in range(1,(df.columns.size+1),1):
    x=list(df[i])
    x_nor=[j/sum(x) for j in x]
    df_nor[i]=x_nor
df_nor=pd.DataFrame.from_dict(df_nor)
#####################7. grouping data ############################## 
GDM=[]
healthy=[]
GDMbefore=[]
GDMafter=[]
healthybefore=[]
healthyafter=[]
df_GDM={}
df_healthy={}
df_GDMbefore={}
df_GDMafter={}
df_healthybefore={}
df_healthyafter={}
for i in range(0,len(peoplename),1):
    cut=peoplename[i]
    if cut[0]=='G':
        ID=re.split('[G,.]',cut)[1]
        if 'G'+ID+'.1' in peoplename and 'G'+ID+'.2' in peoplename:
        
            if cut[len(cut)-1]=='1':
                GDMbefore.append(cut)
                df_GDMbefore[len(df_GDMbefore)+1]=list(df_nor[i+1])
                GDM.append(cut)
                df_GDM[len(df_GDM)+1]=list(df_nor[i+1])
            else:
                if cut[len(cut)-1]=='2':                
                    GDMafter.append(cut)
                    df_GDMafter[len(df_GDMafter)+1]=list(df_nor[i+1])            
                    GDM.append(cut)
                    df_GDM[len(df_GDM)+1]=list(df_nor[i+1])
    else:
        healthy.append(cut)
        df_healthy[len(df_healthy)+1]=list(df_nor[i+1])
        if cut[len(cut)-1]=='1':
            healthybefore.append(cut)
            df_healthybefore[len(df_healthybefore)+1]=list(df_nor[i+1])
        else:
            healthyafter.append(cut)
            df_healthyafter[len(df_healthyafter)+1]=list(df_nor[i+1])          
df_GDM=pd.DataFrame.from_dict(df_GDM)
df_healthy=pd.DataFrame.from_dict(df_healthy)
df_GDMbefore=pd.DataFrame.from_dict(df_GDMbefore)
df_GDMafter=pd.DataFrame.from_dict(df_GDMafter)
df_healthybefore=pd.DataFrame.from_dict(df_healthybefore)
df_healthyafter=pd.DataFrame.from_dict(df_healthyafter)

'Check to see if there are microibome in the group that have 0 abundance after grouping, and remove such microbiomes'
all_0=[]
for i in range(0,len(df_healthybefore),1):
    if len(list(np.nonzero(list(df_healthybefore.iloc[i]))[0]))<2:
        all_0.append(i)
for i in range(0,len(df_healthyafter),1):
    if len(list(np.nonzero(list(df_healthyafter.iloc[i]))[0]))<2:
        all_0.append(i)
for i in range(0,len(df_GDMbefore),1):
    if len(list(np.nonzero(list(df_GDMbefore.iloc[i]))[0]))<2:
        all_0.append(i)
for i in range(0,len(df_GDMafter),1):
    if len(list(np.nonzero(list(df_GDMafter.iloc[i]))[0]))<2:
        all_0.append(i)
        
all_0= set(all_0)#去重复的元素
df_healthybefore=df_healthybefore.drop(labels=all_0, axis=0)
df_healthyafter=df_healthyafter.drop(labels=all_0, axis=0)
df_GDMbefore=df_GDMbefore.drop(labels=all_0, axis=0)
df_GDMafter=df_GDMafter.drop(labels=all_0, axis=0)

microclass_delete=[]
microsname_delete=[]
for i in all_0:
    microclass_delete.append(microclass_cut[i])
    microsname_delete.append(microsname_cut[i])
for i in microclass_delete:
    microclass_cut.remove(i)
for i in microsname_delete:
    microsname_cut.remove(i)

column=[]
for i in range(0,len(df_healthybefore),1):
    column.append(i)
df_healthybefore.index=pd.Series(column)
df_healthyafter.index=pd.Series(column)
df_GDMbefore.index=pd.Series(column)
df_GDMafter.index=pd.Series(column)

##################8. do the final normalization#############################
for i in range(1,(df_healthybefore.columns.size+1),1):
    x=list(df_healthybefore[i])
    x_nor=[j/sum(x) for j in x]
    df_healthybefore[i]=x_nor
for i in range(1,(df_healthyafter.columns.size+1),1):
    x=list(df_healthyafter[i])
    x_nor=[j/sum(x) for j in x]
    df_healthyafter[i]=x_nor
for i in range(1,(df_GDMbefore.columns.size+1),1):
    x=list(df_GDMbefore[i])
    x_nor=[j/sum(x) for j in x]
    df_GDMbefore[i]=x_nor
for i in range(1,(df_GDMafter.columns.size+1),1):
    x=list(df_GDMafter[i])
    x_nor=[j/sum(x) for j in x]
    df_GDMafter[i]=x_nor
