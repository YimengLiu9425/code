# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 22:35:01 2023

@author: Yimeng Liu
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import re

'!!!'
'data needs to be generated in the "data pre-process.py" file first.'
'!!!'
###################################################################
#############import network information########################
###########healthy people microbiome network before diet
'group network'
healthy_before = pd.read_excel('h(W0)_network weight information.xlsx',index_col='Unnamed: 0')

############healthy people microbiome network after diet
'group network'
healthy_after = pd.read_excel('h(W2)_network weight information.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=30
healthy_after_drop={}
for i in range(1,peopsize+1,1): 
    df_healthyafterlink = pd.read_excel('h(W2)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    healthy_after_drop[i]=df_healthyafterlink

############GDM people microbiome network before diet
'group network'
GDM_before = pd.read_excel('g(W0)_network weight information.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=27
GDM_before_drop={}
for i in range(1,peopsize+1,1): 
    df_GDMbeforelink = pd.read_excel('g(W0)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    GDM_before_drop[i]=df_GDMbeforelink

############GDM people microbiome network afte diet
'group network'
GDM_after = pd.read_excel('g(W2)_network weight information.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=27
GDM_after_drop={}
for i in range(1,peopsize+1,1): 
    df_GDMafterlink = pd.read_excel('g(W2)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    GDM_after_drop[i]=df_GDMafterlink


####keep the top 500 links in each network##############3
fix=500
#######h(W0) group network #########
if len(healthy_before)>fix:
    healthy_before_sort =  healthy_before.sort_values(by=0,ascending=False)
    healthy_before_top =  healthy_before_sort[0:fix]
#######h(W2) group network #########
if len(healthy_after)>fix:
    healthy_after_sort =  healthy_after.sort_values(by=0,ascending=False)
    healthy_after_top =  healthy_after_sort[0:fix]
#######g(W0) group network #########
if len(GDM_before)>fix:
    GDM_before_sort =  GDM_before.sort_values(by=0,ascending=False)
    GDM_before_top =  GDM_before_sort[0:fix]
#######g(W2) group network #########
if len(GDM_after)>fix:
    GDM_after_sort =  GDM_after.sort_values(by=0,ascending=False)
    GDM_after_top =  GDM_after_sort[0:fix]
#######h(W2) individual network #########
healthy_after_drop_top={}
for k in healthy_after_drop.keys():
    each=healthy_after_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    healthy_after_drop_top[k]=each_500
#######g(W0) individual network #########
GDM_before_drop_top={}
for k in GDM_before_drop.keys():
    each=GDM_before_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    GDM_before_drop_top[k]=each_500
#######g(W2) individual network #########
GDM_after_drop_top={}
for k in GDM_after_drop.keys():
    each=GDM_after_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    GDM_after_drop_top[k]=each_500



GDMname=['G1.1','G10.1','G11.1','G12.1','G13.1','G14.1','G15.1','G16.1','G17.1','G19.1','G2.1','G20.1','G21.1','G22.1','G23.1','G25.1','G26.1','G27.1','G3.1','G32.1','G28.1','G4.1','G5.1','G6.1','G7.1','G8.1','G9.1']

###################netowrk analysis results#############
'F6(a)'
Jaccard_distance_GDMbefore={}
for i in GDM_before_drop_top.keys():
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    each=GDM_before_drop_top[i]
    count=0 
    for j in each.index:
        if j in GDM_before_top.index:
           count+=1
    Jaccard_distance_GDMbefore[ID]=1-count/(len(each)+len(GDM_before_top.index)-count)
    
J_GBeach_GB={}
for i in sorted(Jaccard_distance_GDMbefore.keys()):
    J_GBeach_GB['g'+str(i)]=Jaccard_distance_GDMbefore[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(J_GBeach_GB.keys()),J_GBeach_GB.values(),color='palevioletred')
plt.xlabel('patients')
plt.ylabel('changes between individual network and whole network')
plt.title('F6(a)')
plt.show()
plt.close()

'F6(b)'
count=0
for j in GDM_before_top.index:
    if j in healthy_before_top.index:
       count+=1
Jaccard_GBHB=count/(len(GDM_before_top.index)+len(healthy_before_top.index)-count) 

Jaccard_distance_GDMbefore_withHB={}
for i in GDM_before_drop_top.keys():
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    each=GDM_before_drop_top[i]
    count=0 
    for j in each.index:
        if j in healthy_before_top.index:
           count+=1
    Jaccard_distance_GDMbefore_withHB[ID]=count/(len(each)+len(healthy_before_top.index)-count)-Jaccard_GBHB
    
J_GBeach_HB={}
for i in sorted(Jaccard_distance_GDMbefore_withHB.keys()):
    J_GBeach_HB['g'+str(i)]=Jaccard_distance_GDMbefore_withHB[i]


plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(J_GBeach_HB.keys()),J_GBeach_HB.values(),color='palevioletred')
plt.xlabel('patients')
plt.ylabel('changes between individual network and healthy network')
plt.title('F6(b)')
plt.grid()
plt.show()
plt.close()

'F6(f)'
Jaccard_distance_GDMafter={}
for i in GDM_after_drop_top.keys():
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    each=GDM_after_drop_top[i]
    count=0 
    for j in each.index:
        if j in GDM_after_top.index:
           count+=1
    Jaccard_distance_GDMafter[ID]=1-count/(len(each)+len(GDM_after_top.index)-count)
    
J_GAeach_GA={}
for i in sorted(Jaccard_distance_GDMafter.keys()):
    J_GAeach_GA['g'+str(i)]=Jaccard_distance_GDMafter[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(J_GAeach_GA.keys()),J_GAeach_GA.values(),color='palevioletred')
plt.xlabel('patients')
plt.ylabel('changes between individual network and whole network')
plt.title('F6(f)')
plt.show()
plt.close()

'F6(g)'
count=0
for j in GDM_after_top.index:
    if j in healthy_after_top.index:
       count+=1
Jaccard_GAHA=count/(len(GDM_after_top.index)+len(healthy_after_top.index)-count) 

Jaccard_distance_GDMafter_withHA={}
for i in GDM_after_drop_top.keys():
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    each=GDM_after_drop_top[i]
    count=0 
    for j in each.index:
        if j in healthy_after_top.index:
           count+=1
    Jaccard_distance_GDMafter_withHA[ID]=count/(len(each)+len(healthy_after_top.index)-count)-Jaccard_GAHA
    
J_GAeach_HA={}
for i in sorted(Jaccard_distance_GDMafter_withHA.keys()):
    J_GAeach_HA['g'+str(i)]=Jaccard_distance_GDMafter_withHA[i]


plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(J_GAeach_HA.keys()),J_GAeach_HA.values(),color='palevioletred')
plt.xlabel('patients')
plt.ylabel('changes between individual network and healthy network')
plt.title('F6(g)')
plt.grid()
plt.show()
plt.close()


###################ncommunity analysis results#############
def Overlap_Jaccard(x,y):
    AandB=[]
    AorB=[]        
    for l in range(0,len(x),1):
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

'F6(c)'
diversity_b_GB_GBeach_mean={}
diversity_b_GB_GBeach_std={}
for i in range(1,(df_GDMbefore.columns.size+1),1):
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    X=list(df_GDMbefore[i])
    X_relative=[l/sum(X) for l in X]
    
    d_each=[]
    for j in range(1,(df_GDMbefore.columns.size+1),1):
        if j!=i:
            Y=list(df_GDMbefore[j])        
            Y_relative=[l/sum(Y) for l in Y]
        
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            d_each.append(dissimilarity)
    
    diversity_b_GB_GBeach_mean[ID]=np.mean(d_each)#  dissimilarity list
    diversity_b_GB_GBeach_std[ID]=np.std(d_each,ddof=1)#  dissimilarity list

dissimilarity_eachGB_GB_mean={}
dissimilarity_eachGB_GB_std={}
for i in sorted(diversity_b_GB_GBeach_mean.keys()):
    dissimilarity_eachGB_GB_mean['g'+str(i)]=diversity_b_GB_GBeach_mean[i]
    dissimilarity_eachGB_GB_std['g'+str(i)]=diversity_b_GB_GBeach_std[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(dissimilarity_eachGB_GB_mean.keys()),list(dissimilarity_eachGB_GB_mean.values()),yerr=list(dissimilarity_eachGB_GB_std.values()),color='olive')
plt.xlabel('patients')
plt.ylabel('distance between individual sample and other samples')
plt.title('F6(c)')
plt.grid()
plt.show()
plt.close()

'F6(d)'
diversity_b_HB_GBeach_mean={}
diversity_b_HB_GBeach_std={}
for i in range(1,(df_GDMbefore.columns.size+1),1):
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    X=list(df_GDMbefore[i])
    X_relative=[l/sum(X) for l in X]
    
    d_each=[]
    for j in range(1,(df_healthybefore.columns.size+1),1):
        Y=list(df_healthybefore[j])        
        Y_relative=[l/sum(Y) for l in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        d_each.append(dissimilarity)
    
    diversity_b_HB_GBeach_mean[ID]=np.mean(d_each)#  dissimilarity list
    diversity_b_HB_GBeach_std[ID]=np.std(d_each,ddof=1)#  dissimilarity list

dissimilarity_eachGB_HB_mean={}
dissimilarity_eachGB_HB_std={}
for i in sorted(diversity_b_HB_GBeach_mean.keys()):
    dissimilarity_eachGB_HB_mean['g'+str(i)]=diversity_b_HB_GBeach_mean[i]
    dissimilarity_eachGB_HB_std['g'+str(i)]=diversity_b_HB_GBeach_std[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(dissimilarity_eachGB_HB_mean.keys()),list(dissimilarity_eachGB_HB_mean.values()),yerr=list(dissimilarity_eachGB_HB_std.values()),color='olive')
plt.xlabel('patients')
plt.ylabel('distance between individual sample and healthy samples')
plt.title('F6(d)')
plt.grid()
plt.show()
plt.close()

'F6(h)'
diversity_b_GA_GAeach_mean={}
diversity_b_GA_GAeach_std={}
for i in range(1,(df_GDMafter.columns.size+1),1):
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    X=list(df_GDMafter[i])
    X_relative=[l/sum(X) for l in X]
    
    d_each=[]
    for j in range(1,(df_GDMafter.columns.size+1),1):
        if j!=i:
            Y=list(df_GDMafter[j])        
            Y_relative=[l/sum(Y) for l in Y]
        
            Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
            overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
            overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
            
            dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
            d_each.append(dissimilarity)
    
    diversity_b_GA_GAeach_mean[ID]=np.mean(d_each)#  dissimilarity list
    diversity_b_GA_GAeach_std[ID]=np.std(d_each,ddof=1)#  dissimilarity list

dissimilarity_eachGA_GA_mean={}
dissimilarity_eachGA_GA_std={}
for i in sorted(diversity_b_GA_GAeach_mean.keys()):
    dissimilarity_eachGA_GA_mean['g'+str(i)]=diversity_b_GA_GAeach_mean[i]
    dissimilarity_eachGA_GA_std['g'+str(i)]=diversity_b_GA_GAeach_std[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(dissimilarity_eachGA_GA_mean.keys()),list(dissimilarity_eachGA_GA_mean.values()),yerr=list(dissimilarity_eachGA_GA_std.values()),color='olive')
plt.xlabel('patients')
plt.ylabel('distance between individual sample and other samples')
plt.title('F6(h)')
plt.grid()
plt.show()
plt.close()

'F6(i)'
diversity_b_HA_GAeach_mean={}
diversity_b_HA_GAeach_std={}
for i in range(1,(df_GDMafter.columns.size+1),1):
    patient=GDMname[i-1]
    ID=int(re.split('[G,.]',GDMname[i-1])[1])
    X=list(df_GDMafter[i])
    X_relative=[l/sum(X) for l in X]
    
    d_each=[]
    for j in range(1,(df_healthyafter.columns.size+1),1):
        Y=list(df_healthyafter[j])        
        Y_relative=[l/sum(Y) for l in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        d_each.append(dissimilarity)
    
    diversity_b_HA_GAeach_mean[ID]=np.mean(d_each)#  dissimilarity list
    diversity_b_HA_GAeach_std[ID]=np.std(d_each,ddof=1)#  dissimilarity list

dissimilarity_eachGA_HA_mean={}
dissimilarity_eachGA_HA_std={}
for i in sorted(diversity_b_HA_GAeach_mean.keys()):
    dissimilarity_eachGA_HA_mean['g'+str(i)]=diversity_b_HA_GAeach_mean[i]
    dissimilarity_eachGA_HA_std['g'+str(i)]=diversity_b_HA_GAeach_std[i]

plt.figure(figsize=(15,5),dpi=450)
plt.bar(list(dissimilarity_eachGA_HA_mean.keys()),list(dissimilarity_eachGA_HA_mean.values()),yerr=list(dissimilarity_eachGA_HA_std.values()),color='olive')
plt.xlabel('patients')
plt.ylabel('distance between individual sample and healthy samples')
plt.title('F6(i)')
plt.grid()
plt.show()
plt.close()
    





