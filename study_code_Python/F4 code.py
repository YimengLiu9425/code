# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 17:07:59 2023

@author: Yimeng Liu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

'!!!'
'data needs to be generated in the "data pre-process.py" file first.'
'!!!'
###################################################################
#############import network information########################
###########healthy people microbiome network before diet
healthy_before = pd.read_excel('h(W0)_network weight information.xlsx',index_col='Unnamed: 0')

############healthy people microbiome network after diet
healthy_after = pd.read_excel('h(W2)_network weight information.xlsx',index_col='Unnamed: 0')

############GDM people microbiome network before diet
GDM_before = pd.read_excel('g(W0)_network weight information.xlsx',index_col='Unnamed: 0')

############GDM people microbiome network afte diet
GDM_after = pd.read_excel('g(W2)_network weight information.xlsx',index_col='Unnamed: 0')

####keep the top 500 links in each network##############3
fix=500
#######h(W0)#########
if len(healthy_before)>fix:
    healthy_before_sort =  healthy_before.sort_values(by=0,ascending=False)
    healthy_before_top =  healthy_before_sort[0:fix]
#######h(W2)#########
if len(healthy_after)>fix:
    healthy_after_sort =  healthy_after.sort_values(by=0,ascending=False)
    healthy_after_top =  healthy_after_sort[0:fix]
#######g(W0)#########
if len(GDM_before)>fix:
    GDM_before_sort =  GDM_before.sort_values(by=0,ascending=False)
    GDM_before_top =  GDM_before_sort[0:fix]
#######g(W2)#########
if len(GDM_after)>fix:
    GDM_after_sort =  GDM_after.sort_values(by=0,ascending=False)
    GDM_after_top =  GDM_after_sort[0:fix]

############1. top 500 h(W0) and h(W2)#############
count=0
for i in healthy_before_top.index:
    if i in healthy_after_top.index:
        count+=1
overlap_h=count/(len(healthy_before_top)+len(healthy_after_top)-count)
print(overlap_h)
############2. top 500 g(W0) and g(W2)#############
count=0
for i in GDM_before_top.index:
    if i in GDM_after_top.index:
        count+=1
overlap_g=count/(len(GDM_before_top)+len(GDM_after_top)-count)
print(overlap_g)
###########shuffle_overlap##########
alllink_name=[]
for ii in range(0,101,1):
    for jj in range((ii+1),101,1):
        alllink_name.append((ii,jj))
shuffle_time=1000
Jaccard_shuffle=[]
for jj in range(0,shuffle_time,1):
    if jj%100==0:
        print(jj)
    before_shuffle=list(random.sample(alllink_name,len(healthy_before_top)))
    after_shuffle=list(random.sample(alllink_name,len(healthy_after_top)))
    count=0
    for ii in before_shuffle:
        if ii in after_shuffle:
            count=count+1
    Jaccard_shuffle.append(count/(len(before_shuffle)+len(after_shuffle)-count))

a=plt.hist(Jaccard_shuffle,weights=np.zeros_like(Jaccard_shuffle) + 1./ len(Jaccard_shuffle), bins=10,histtype="stepfilled", alpha=.8,color='red')
xx=[]
for h in range(0,10,1):
    xx.append((a[1][h]+a[1][h+1])/2)
plt.bar(xx,list(a[0]),width=0.004,edgecolor='pink',color='pink',label='random')
plt.xlim(0,overlap_h+0.09)
#plt.ylim(0,0.27)
plt.annotate('', xy=(overlap_h,0), xytext=(overlap_h, 0.15),fontsize=10,arrowprops=dict(facecolor='blue', shrink=0.05,edgecolor='blue'))
plt.text(overlap_h+0.01, 0.13,round(overlap_h,3),fontsize=15)
plt.text(overlap_h+0.01, 0.16,'(H(W0),H(W2))',fontsize=12)
plt.annotate('', xy=(overlap_g, 0), xytext=(overlap_g, 0.15),fontsize=10,arrowprops=dict(facecolor='orange', shrink=0.05,edgecolor='orange'))
plt.text(overlap_g-0.04, 0.13,round(overlap_g,3),fontsize=15)
plt.text(overlap_g-0.07, 0.16,'(G(W0),G(W2))',fontsize=12)
plt.legend()
plt.xlabel('Jaccard similarity')
plt.ylabel('Frequency')
plt.show()
plt.close()
