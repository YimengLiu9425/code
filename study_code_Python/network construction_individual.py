# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:32:37 2023

@author: Yimeng Liu
"""

import numpy as np
import pandas as pd
import time
import random
import networkx as nx

'!!!'
'data needs to be generated in the "data pre-process.py" file first.'
'!!!'
###################################################################

def network_construction_individual(data,W_cut,peopsize):
    df_allC0andW_all={}
    edge_weight_all={}
    edge_weight_w_all={}
    for ss in range(1,peopsize+1,1): 
        print('ss=',ss)
        ################选出一部分人作为subset
        subject_No=list(data.columns)
        subject_No.remove(ss)
        subset_before=subject_No
        subset_before = pd.DataFrame(subset_before)
        
        ############################建网
        subcell=list(subset_before[0])
        cellset={}#子细胞集合所对应的的gene表
        for j in range(0,len(subcell),1):
            cellset[j+1]=data[subcell[j]]
        cellset=pd.DataFrame.from_dict(cellset)#这个网络对应的细胞-gene表 
        
    
        time_start=time.time()#time_count
        G = nx.Graph()#建网
        G.add_nodes_from(list(cellset.columns))#添加点(从1开始的)
        edge_weight={} #边的两端和权重
        edge_weight_w={} #边的两端和权重
        C_true=[]###所有边的权重，用来检查网络有没有建对
        W_true=[]
        W_all=[]###所有的pair的W，用来检查网络有没有建对
        C0_all=[]###所有的pair的C0，用来检查网络有没有建对
        for m in range(0,len(cellset),1):
            if m % 10 == 0:
                print('m=',m)  ###判断进度          
            x=cellset.iloc[m]
            for n in range((m+1),len(cellset),1):
                y=cellset.iloc[n]
                Pearson=pd.DataFrame({'A':list(x),'B':list(y)})
                C0=Pearson.corr('pearson')['B']['A']#计算两个gene之间的相关系数        
                C0_all.append(C0)#用来检验
                ####################################
                ######计算Significant link test#####
                C_shuffle=[]
                shuffletime=1000        
                x_shuffle=[]
                x_shuffle=list(x)
                y_shuffle=[]
                y_shuffle=list(y)
        
                for s in range(0,shuffletime,1):
                    random.shuffle(x_shuffle)
                    random.shuffle(y_shuffle)
                    Pearson=pd.DataFrame({'A':x_shuffle,'B':y_shuffle})
                    shuffle=Pearson.corr('pearson')['B']['A']
                    C_shuffle.append(shuffle)#1000次shuffle
                C_shuffle_mean = np.mean(C_shuffle)
                C_shuffle_std = np.std(C_shuffle,ddof=1)
                W=(C0-C_shuffle_mean)/C_shuffle_std
                W_all.append(W)#用来检验        
                if W>W_cut:
                     G.add_edge(m,n,weight=C0)
                     edge_weight[(m,n)]=C0#所有边，可以排序选2%
                     edge_weight_w[(m,n)]=W#所有边，可以排序选2%
                     C_true.append(C0)
                     W_true.append(W)
        df_allC0andW = pd.DataFrame({'C_all':C0_all,'W_all':W_all})
        edge_weight=pd.DataFrame.from_dict(edge_weight,orient='index') 
        edge_weight_w=pd.DataFrame.from_dict(edge_weight_w,orient='index') 
        time_end=time.time()
        print('totally cost',time_end-time_start)
        df_allC0andW_all[ss]=df_allC0andW
        edge_weight_all[ss]=edge_weight
        edge_weight_w_all[ss]=edge_weight_w
    return df_allC0andW_all,edge_weight_all,edge_weight_w_all


result_hw2_individual=network_construction_individual(df_healthyafter,1,30)
df_allC0andW_all=result_hw2_individual[0]
edge_weight_all=result_hw2_individual[1]
edge_weight_w_all=result_hw2_individual[2]
for i in df_allC0andW_all.keys():
    df_allC0andW=df_allC0andW_all[i]
    edge_weight=edge_weight_all[i]
    edge_weight_w=edge_weight_w_all[i]
    df_allC0andW.to_excel ('h(W2)_indivual %d network allC0andW.xlsx'%(i))
    edge_weight.to_excel('h(W2)_indivual %d network weight information.xlsx'%(i))
    edge_weight_w.to_excel('h(W2)_indivual %d network weight information_w.xlsx'%(i))

result_gw0_individual=network_construction_individual(df_GDMbefore,1,27)
df_allC0andW_all=result_gw0_individual[0]
edge_weight_all=result_gw0_individual[1]
edge_weight_w_all=result_gw0_individual[2]
for i in df_allC0andW_all.keys():
    df_allC0andW=df_allC0andW_all[i]
    edge_weight=edge_weight_all[i]
    edge_weight_w=edge_weight_w_all[i]
    df_allC0andW.to_excel ('g(W0)_indivual %d network allC0andW.xlsx'%(i))
    edge_weight.to_excel('g(W0)_indivual %d network weight information.xlsx'%(i))
    edge_weight_w.to_excel('g(W0)_indivual %d network weight information_w.xlsx'%(i))

result_gw2_individual=network_construction_individual(df_GDMafter,1,27)
df_allC0andW_all=result_gw2_individual[0]
edge_weight_all=result_gw2_individual[1]
edge_weight_w_all=result_gw2_individual[2]
for i in df_allC0andW_all.keys():
    df_allC0andW=df_allC0andW_all[i]
    edge_weight=edge_weight_all[i]
    edge_weight_w=edge_weight_w_all[i]
    df_allC0andW.to_excel ('g(W2)_indivual %d network allC0andW.xlsx'%(i))
    edge_weight.to_excel('g(W2)_indivual %d network weight information.xlsx'%(i))
    edge_weight_w.to_excel('g(W2)_indivual %d network weight information_w.xlsx'%(i))




