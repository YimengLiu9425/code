# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 21:04:16 2023

@author: Yimeng Liu
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import math
import seaborn as sns

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


################F5(b): network analysis##############
J_cross={}
###GBHB
J_cross['H(W0)-G(W0)']={}
for ii in GDM_before_drop_top.keys():
    each=GDM_before_drop_top[ii]
    count=0
    for jj in each.index:
        if jj in healthy_before_top.index:
            count+=1
    J_cross['H(W0)-G(W0)'][ii]=count/(len(each)+len(healthy_before_top.index)-count)
print('H(W0)-G(W0)',np.mean(list(J_cross['H(W0)-G(W0)'].values())))
###GAHB
J_cross['H(W0)-G(W2)']={}
for ii in GDM_after_drop_top.keys():
    each=GDM_after_drop_top[ii]
    count=0
    for jj in each.index:
        if jj in healthy_before_top.index:
            count+=1
    J_cross['H(W0)-G(W2)'][ii]=count/(len(each)+len(healthy_before_top.index)-count)
print('H(W0)-G(W2)',np.mean(list(J_cross['H(W0)-G(W2)'].values())))
###GBHA
J_cross['H(W2)-G(W0)']={}
for ii in GDM_before_drop_top.keys():
    each=GDM_before_drop_top[ii]
    count=0
    for jj in each.index:
        if jj in healthy_after_top.index:
            count+=1
    J_cross['H(W2)-G(W0)'][ii]=count/(len(each)+len(healthy_after_top.index)-count)
print('H(W2)-G(W0)',np.mean(list(J_cross['H(W2)-G(W0)'].values())))
###GAHA
J_cross['H(W2)-G(W2)']={}
for ii in GDM_after_drop_top.keys():
    each=GDM_after_drop_top[ii]
    count=0
    for jj in each.index:
        if jj in healthy_after_top.index:
            count+=1
    J_cross['H(W2)-G(W2)'][ii]=count/(len(each)+len(healthy_after_top.index)-count)
print('H(W2)-G(W2)',np.mean(list(J_cross['H(W2)-G(W2)'].values())))

J_cross = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in J_cross.items()]))
my_pal = {"H(W0)-G(W0)": "darkgreen", "H(W0)-G(W2)": "palegreen", "H(W2)-G(W0)": "red","H(W2)-G(W2)": "lightcoral"}
sns.violinplot(data=J_cross,palette=my_pal)
plt.ylabel('Jaccard simialrity')
plt.show()
#####################significant test############################
###Wilcoxon Rank Sum test###
import scipy.stats as ss
print('hW0-gW0 & hW0-gW2',ss.ranksums(J_cross['H(W0)-G(W0)'], J_cross['H(W0)-G(W2)']))
print('hW2-gW0 & hW2-gW2',ss.ranksums(J_cross['H(W2)-G(W0)'], J_cross['H(W2)-G(W2)']))


##################F5(c): community analysis###############################
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
###########################dissimilarity_nature########################
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
##########################B diveristy###########
dissimilarity_cross={}
diversity_b_HB_GB=[]
diversity_b_HB_GA=[]
diversity_b_HA_GB=[]
diversity_b_HA_GA=[]

for i in range(1,(df_GDMbefore.columns.size+1),1):
    X=list(df_GDMbefore[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthybefore.columns.size+1),1):
        Y=list(df_healthybefore[j])        
        Y_relative=[k/sum(Y) for k in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        each.append(dissimilarity)
    diversity_b_HB_GB.append(np.mean(each))#  dissimilarity list
dissimilarity_cross['h(W0)-g(W0)']=diversity_b_HB_GB 

for i in range(1,(df_GDMafter.columns.size+1),1):
    X=list(df_GDMafter[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthybefore.columns.size+1),1):
        Y=list(df_healthybefore[j])        
        Y_relative=[k/sum(Y) for k in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        each.append(dissimilarity)
    diversity_b_HB_GA.append(np.mean(each))#  dissimilarity list
dissimilarity_cross['h(W0)-g(W2)']=diversity_b_HB_GA 

 
for i in range(1,(df_GDMbefore.columns.size+1),1):
    X=list(df_GDMbefore[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthyafter.columns.size+1),1):
        Y=list(df_healthyafter[j])        
        Y_relative=[k/sum(Y) for k in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        each.append(dissimilarity)
    diversity_b_HA_GB.append(np.mean(each))#  dissimilarity list
dissimilarity_cross['h(W2)-g(W0)']=diversity_b_HA_GB 

for i in range(1,(df_GDMafter.columns.size+1),1):
    X=list(df_GDMafter[i])
    X_relative=[l/sum(X) for l in X]
    each=[]
    for j in range(1,(df_healthyafter.columns.size+1),1):
        Y=list(df_healthyafter[j])        
        Y_relative=[k/sum(Y) for k in Y]
        
        Overlap_pair=Overlap_Jaccard(X_relative,Y_relative)[0]
        overlap_part=Overlap_Jaccard(X_relative,Y_relative)[2]
        overlap_lenth=Overlap_Jaccard(X_relative,Y_relative)[1]
        
        dissimilarity=Dissimilarity_Amir(X_relative,Y_relative)
        each.append(dissimilarity)
    diversity_b_HA_GA.append(np.mean(each))#  dissimilarity list
dissimilarity_cross['h(W2)-g(W2)']=diversity_b_HA_GA 

dissimilarity_cross = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dissimilarity_cross.items()]))
my_pal = {"h(W0)-g(W0)": "darkgreen", "h(W0)-g(W2)": "palegreen", "h(W2)-g(W0)": "red","h(W2)-g(W2)": "lightcoral"}
sns.violinplot(data=dissimilarity_cross,palette=my_pal)
plt.ylabel('rJSD')

#####################significant test############################
###Wilcoxon Rank Sum test###
import scipy.stats as ss
print('hW0-gW0 & hW0-gW2',ss.ranksums(dissimilarity_cross['h(W0)-g(W0)'], dissimilarity_cross['h(W0)-g(W2)']))
print('hW2-gW0 & hW2-gW2',ss.ranksums(dissimilarity_cross['h(W2)-g(W0)'], dissimilarity_cross['h(W2)-g(W2)']))





