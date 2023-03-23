# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:54:15 2023

@author: Yimeng Liu
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 22:23:08 2023

@author: Yimeng Liu
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import math
import re
import seaborn as sns


'!!!'
'data needs to be generated in the "data pre-process.py" file first.'
'!!!'
###################################################################

#####################F3(a):PCOA #############################
'Output: 1) OTU table, 2) PCOA distance, 3)grouping condition'
'The output data will be computed in the R project("PCOA_code_R") to generate the PCOA result'

##############1) OTU data 
df_healthybefore.columns=range(1,len(df_healthybefore.columns)+1,1)
df_healthyafter.columns=range(1,len(df_healthyafter.columns)+1,1)
df_GDMbefore.columns=range(1,len(df_GDMbefore.columns)+1,1)
df_GDMafter.columns=range(1,len(df_GDMafter.columns)+1,1)
    
read=pd.merge(df_healthybefore,df_healthyafter,left_index=True,right_index=True)
read=pd.merge(read,df_GDMbefore,left_index=True,right_index=True)
read=pd.merge(read,df_GDMafter,left_index=True,right_index=True)
read.to_csv('otu_table.txt',sep='\t',index=True)
#############2) PCOA distance _rJSD distance
def Overlap_Jaccard(x,y):
    AandB=[]
    AorB=[]        
    for l in range(0,len(X_relative),1):
        if x[l]!=0 and y[l]!=0:
            AandB.append(l)
            AorB.append(l)
        else:
            if x[l]==0 and y[l]!=0:
                AorB.append(l)
            else:
                if x[l]!=0 and y[l]==0:
                    AorB.append(l)
                else:
                    continue
    Overlap_pair=len(AandB)/len(AorB)
    return Overlap_pair,len(AandB),AandB

def Dissimilarity_Amir(X,Y):    
    XS=[]
    YS=[]
    m=[]
    Dklxm_sub=[]
    Dklym_sub=[]
    XS_relative=[]
    YS_relative=[]
    #for b in S_index:
    for b in overlap_part:
        XS.append(X[b])
        YS.append(Y[b])
    XS_relative=[k/sum(XS) for k in XS]
    YS_relative=[k/sum(YS) for k in YS]
    #for d in range(0,len(S_index),1):
    for d in range(0,overlap_lenth,1):
        m.append((XS_relative[d]+YS_relative[d])/2)
        Dklxm_sub.append(XS_relative[d]*(math.log((XS_relative[d]/m[d]),math.e)))
        Dklym_sub.append(YS_relative[d]*(math.log((YS_relative[d]/m[d]),math.e)))
    Dklxm=sum( Dklxm_sub)
    Dklym=sum( Dklym_sub)
    Dissimilarity_pair=((Dklxm+Dklym)/2)**0.5    
    return Dissimilarity_pair

diversity_b_all={}
for i in read.columns:
    X=list(read[i])
    X_relative=[l/sum(X) for l in X]
    diversity_b_each=[]
    for j in read.columns:
        Y=list(read[j])        
        Y_relative=[k/sum(Y) for k in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
       
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        diversity_b_each.append(dissimilarity)#  dissimilarity list
    diversity_b_all[i]=diversity_b_each
diversity_b_all=pd.DataFrame.from_dict(diversity_b_all)
diversity_b_all.index=pd.Series(diversity_b_all.columns)
diversity_b_all.to_csv('distance.txt',sep='\t',index=True)
#############3) grouping condition
name=list(read.columns)
people=[]
disease=[]
week=[]
for i in range(0,len(name),1):
    cut=name[i]
    if cut[0]=='G':
        if cut[len(cut)-1]=='1':
            people.append('g(W0)')
            disease.append('GDM')
            week.append('W0')
        else:
            people.append('g(W2)')
            disease.append('GDM')
            week.append('W2')
    else:
        if cut[len(cut)-1]=='1':
            people.append('h(W0)')
            disease.append('healthy')
            week.append('W0')
        else:
            people.append('h(W2)')
            disease.append('healthy')
            week.append('W2')
group = pd.DataFrame({'name':name,'type':people,'disease':disease,'week':week})
group.to_csv('group_type.txt',sep='\t',index=False)

########Import the result of PCOA and draw picture ############
'This results can also be drawn in R project!'
PCOA=pd.read_csv('PCOA result.csv')#This file be generated in R project
x=list(PCOA['PCoA1'])
y=list(PCOA['PCoA2'])
Name=list(PCOA['names'])

hb_x = []
hb_y = []
ha_x = []
ha_y = []
gb_x = []
gb_y = []
ga_x = []
ga_y = []
for i in range(len(Name)):         
    if Name[i] == 'h(W0)':    #根据标签进行数据分类
        hb_x.append(x[i])  
        hb_y.append(y[i])
 
    if Name[i] == 'h(W2)':
        ha_x.append(x[i])
        ha_y.append(y[i])
 
    if Name[i] == 'g(W0)':
        gb_x.append(x[i])
        gb_y.append(y[i])
        
    if Name[i] == 'g(W2)':
        ga_x.append(x[i])
        ga_y.append(y[i])
 
plt.scatter(list(hb_x), list(hb_y),c='b', marker='.',label='h(W0)')
plt.scatter(ha_x, ha_y,  c='b', marker='x', label='h(W2)')
plt.scatter(gb_x, gb_y,  c='orange', marker='.', label='g(W0)') 
plt.scatter(ga_x, ga_y,  c='orange', marker='x',label='g(W2)')
plt.legend()
plt.xlabel('PCOA_1')
plt.ylabel('PCOA_2')
plt.show()



###################F3(b):β diversity in each group##################
diversity_b_healthybefore=[]
diversity_b_healthyafter=[]
diversity_b_GDMbefore=[]
diversity_b_GDMafter=[]

for i in range(1,(df_healthybefore.columns.size+1),1):
    X=list(df_healthybefore[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthybefore.columns.size+1),1):
        if j!=i:
            Y=list(df_healthybefore[j])        
            Y_relative=[l/sum(Y) for l in Y]
            
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            each.append(dissimilarity)
    diversity_b_healthybefore.append(np.mean(each))#  dissimilarity list
    
for i in range(1,(df_healthyafter.columns.size+1),1):
    X=list(df_healthyafter[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthyafter.columns.size+1),1):
        if j!=i:
            Y=list(df_healthyafter[j])        
            Y_relative=[l/sum(Y) for l in Y]
            
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            each.append(dissimilarity)
    diversity_b_healthyafter.append(np.mean(each))#  dissimilarity list
 
for i in range(1,(df_GDMbefore.columns.size+1),1):
    X=list(df_GDMbefore[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_GDMbefore.columns.size+1),1):
        if j!=i:
            Y=list(df_GDMbefore[j])        
            Y_relative=[l/sum(Y) for l in Y]
            
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            each.append(dissimilarity)
    diversity_b_GDMbefore.append(np.mean(each))#  dissimilarity list
 
for i in range(1,(df_GDMafter.columns.size+1),1):
    X=list(df_GDMafter[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_GDMafter.columns.size+1),1):
        if j!=i:
            Y=list(df_GDMafter[j])        
            Y_relative=[l/sum(Y) for l in Y]
            
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            each.append(dissimilarity)
    diversity_b_GDMafter.append(np.mean(each))#  dissimilarity list

diversity_b={} 
diversity_b['h(W0)']=diversity_b_healthybefore
diversity_b['h(W2)']=diversity_b_healthyafter
diversity_b['g(W0)']=diversity_b_GDMbefore
diversity_b['g(W2)']=diversity_b_GDMafter
df_diversity_b = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in diversity_b.items()]))

my_pal = {"h(W0)": "b", "h(W2)": "lightblue", "g(W0)": "darkorange","g(W2)": "papayawhip"}
sns.violinplot(data=df_diversity_b,palette=my_pal)
plt.ylabel('β diversity in group')
plt.show()











