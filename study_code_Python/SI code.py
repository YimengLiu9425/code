# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 04:49:32 2023

@author: Yimeng Liu
"""



import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import random
import seaborn as sns
'!!!'
'data needs to be generated in the "data pre-process.py" file first.'
'!!!'
###################################################################

#############import network information########################
###########healthy people microbiome network before diet
'group network'
healthy_before = pd.read_excel('h(W0)_network weight information.xlsx',index_col='Unnamed: 0')
healthy_before_w = pd.read_excel('h(W0)_network weight information_w.xlsx',index_col='Unnamed: 0')

############healthy people microbiome network after diet
'group network'
healthy_after = pd.read_excel('h(W2)_network weight information.xlsx',index_col='Unnamed: 0')
healthy_after_w = pd.read_excel('h(W2)_network weight information_w.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=30
healthy_after_drop={}
healthy_after_drop_w={}
for i in range(1,peopsize+1,1): 
    df_healthyafterlink = pd.read_excel('h(W2)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    df_healthyafterlink_w = pd.read_excel('h(W2)_indivual %d network weight information_w.xlsx'%(i),index_col='Unnamed: 0')
    healthy_after_drop[i]=df_healthyafterlink
    healthy_after_drop_w[i]=df_healthyafterlink_w 

############GDM people microbiome network before diet
'group network'
GDM_before = pd.read_excel('g(W0)_network weight information.xlsx',index_col='Unnamed: 0')
GDM_before_w = pd.read_excel('g(W0)_network weight information_w.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=27
GDM_before_drop={}
GDM_before_drop_w={}
for i in range(1,peopsize+1,1): 
    df_GDMbeforelink = pd.read_excel('g(W0)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    df_GDMbeforelink_w = pd.read_excel('g(W0)_indivual %d network weight information_w.xlsx'%(i),index_col='Unnamed: 0')
    GDM_before_drop[i]=df_GDMbeforelink
    GDM_before_drop_w[i]=df_GDMbeforelink_w 

############GDM people microbiome network afte diet
'group network'
GDM_after = pd.read_excel('g(W2)_network weight information.xlsx',index_col='Unnamed: 0')
GDM_after_w = pd.read_excel('g(W2)_network weight information_w.xlsx',index_col='Unnamed: 0')

'individual network'
peopsize=27
GDM_after_drop={}
GDM_after_drop_w={}
for i in range(1,peopsize+1,1): 
    df_GDMafterlink = pd.read_excel('g(W2)_indivual %d network weight information.xlsx'%(i),index_col='Unnamed: 0')
    df_GDMafterlink_w = pd.read_excel('g(W2)_indivual %d network weight information_w.xlsx'%(i),index_col='Unnamed: 0')
    GDM_after_drop[i]=df_GDMafterlink
    GDM_after_drop_w[i]=df_GDMafterlink_w 

'''
######计算原文章的结果——top 500 links###################
####生成只有top 500的数据##############3
fix=500
#######HB#########
if len(healthy_before)>fix:
    healthy_before_sort =  healthy_before.sort_values(by=0,ascending=False)
    healthy_before_top =  healthy_before_sort[0:fix]
#######HA#########
if len(healthy_after)>fix:
    healthy_after_sort =  healthy_after.sort_values(by=0,ascending=False)
    healthy_after_top =  healthy_after_sort[0:fix]
#######GB#########
if len(GDM_before)>fix:
    GDM_before_sort =  GDM_before.sort_values(by=0,ascending=False)
    GDM_before_top =  GDM_before_sort[0:fix]
#######GA#########
if len(GDM_after)>fix:
    GDM_after_sort =  GDM_after.sort_values(by=0,ascending=False)
    GDM_after_top =  GDM_after_sort[0:fix]
########HA drop###########
healthy_after_drop_top={}
for k in healthy_after_drop.keys():
    each=healthy_after_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    healthy_after_drop_top[k]=each_500
########GB drop###########
GDM_before_drop_top={}
for k in GDM_before_drop.keys():
    each=GDM_before_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    GDM_before_drop_top[k]=each_500
########GA drop###########
GDM_after_drop_top={}
for k in GDM_after_drop.keys():
    each=GDM_after_drop[k]
    if len(each)>fix:
        each_sort = each.sort_values(by=0,ascending=False)
        each_500 =  each_sort[0:fix]
    GDM_after_drop_top[k]=each_500
'''


########################F1#########################
W=[1,1.5,2,2.5,3,3.5]
link_healthy_before_W={}
link_healthy_after_W={}
link_GDM_before_W={}
link_GDM_after_W={}
for w in W:
    print(w)
    ##HB
    count=0
    for i in healthy_before_w.index:
        if healthy_before_w[0][i]>w:
            count+=1
    link_healthy_before_W[w]=count
    ##HA
    count=0
    for i in healthy_after_w.index:
        if healthy_after_w[0][i]>w:
            count+=1
    link_healthy_after_W[w]=count
    ##GB
    count=0
    for i in GDM_before_w.index:
        if GDM_before_w[0][i]>w:
            count+=1
    link_GDM_before_W[w]=count
    ##GA
    count=0
    for i in GDM_after_w.index:
        if GDM_after_w[0][i]>w:
            count+=1
    link_GDM_after_W[w]=count

###############plot################
barWidth = 0.1
W1 = W
W2 = [x + barWidth for x in W1] 
W3 = [x + barWidth for x in W2] 
W4 = [x + barWidth for x in W3] 

plt.bar(W1, link_healthy_before_W.values(), width = barWidth, color = 'blue', edgecolor = 'black', capsize=7, label='h(W0)') 
plt.bar(W2, link_healthy_after_W.values(), width = barWidth, color = 'white', edgecolor = 'blue', capsize=7, label='h(W2)') 
plt.bar(W3, link_GDM_before_W.values(), width = barWidth, color = 'orange', edgecolor = 'black', capsize=7, label='g(W0)') 
plt.bar(W4, link_GDM_after_W.values(), width = barWidth, color = 'white', edgecolor = 'orange', capsize=7, label='g(W2)') 
# general layout 
plt.xticks([r + 1.5*barWidth for r in W], W) 
plt.xlabel('W')
plt.ylabel('amount of links') 
plt.grid()
plt.legend() 
plt.show()



########################F2############################
Range=[i/10 for i in range(10,36,1)]
link_healthy_before_threshold={}
link_healthy_after_threshold={}
link_healthy_after_drop_threshold={}
link_GDM_before_threshold={}
link_GDM_before_drop_threshold={}
link_GDM_after_threshold={}
link_GDM_after_drop_threshold={}
for w in Range:
    print(w)
    ##HB
    link=[]
    for i in healthy_before_w.index:
        if healthy_before_w[0][i]>w:
            link.append(i)
    link_healthy_before_threshold[w]=link
    ##HA
    link=[]
    for i in healthy_after_w.index:
        if healthy_after_w[0][i]>w:
            link.append(i)
    link_healthy_after_threshold[w]=link
    ##HA_drop
    link_drop={}
    for i in healthy_after_drop_w.keys():
        each=healthy_after_drop_w[i]
        link=[]
        for j in each.index:
            if each[0][j]>w:
                link.append(j)
        link_drop[i]=link
    link_healthy_after_drop_threshold[w]=link_drop
    ##GB
    link=[]
    for i in GDM_before_w.index:
        if GDM_before_w[0][i]>w:
            link.append(i)
    link_GDM_before_threshold[w]=link
    ##GB_drop
    link_drop={}
    for i in GDM_before_drop_w.keys():
        each=GDM_before_drop_w[i]
        link=[]
        for j in each.index:
            if each[0][j]>w:
                link.append(j)
        link_drop[i]=link
    link_GDM_before_drop_threshold[w]=link_drop
    ##GA
    link=[]
    for i in GDM_after_w.index:
        if GDM_after_w[0][i]>w:
            link.append(i)
    link_GDM_after_threshold[w]=link
    ##GA_drop
    link_drop={}
    for i in GDM_after_drop_w.keys():
        each=GDM_after_drop_w[i]
        link=[]
        for j in each.index:
            if each[0][j]>w:
                link.append(j)
        link_drop[i]=link
    link_GDM_after_drop_threshold[w]=link_drop


alllink_name=[]
for ii in range(0,len(df_healthybefore),1):
    for jj in range((ii+1),len(df_healthybefore),1):
        alllink_name.append((ii,jj))

GBHB_mean=[]
GBHA_mean=[]
GAHB_mean=[]
GAHA_mean=[]
GBHB_shuffle_mean=[]
GBHA_shuffle_mean=[]
GAHB_shuffle_mean=[]
GAHA_shuffle_mean=[]
GBHB_std=[]
GBHA_std=[]
GAHB_std=[]
GAHA_std=[]
GBHB_shuffle_std=[]
GBHA_shuffle_std=[]
GAHB_shuffle_std=[]
GAHA_shuffle_std=[]
X=[i/10 for i in range(10,36,1)]
for w in X:
    print(w)
    link_hb=link_healthy_before_threshold[w]
    link_ha=link_healthy_after_threshold[w]
    link_ha_drop=link_healthy_after_drop_threshold[w]
    link_gb=link_GDM_before_threshold[w]
    link_gb_drop=link_GDM_before_drop_threshold[w]
    link_ga=link_GDM_after_threshold[w]
    link_ga_drop=link_GDM_after_drop_threshold[w]
    
    fix=min(len(link_hb),len(link_ha),len(link_gb),min(list(len(link_ha_drop[l]) for l in link_ha_drop.keys())),min(list(len(link_gb_drop[l]) for l in link_gb_drop.keys())),min(list(len(link_ga_drop[l]) for l in link_ga_drop.keys())))
    print(fix)
    
    if len(link_hb)!=fix:
        weight={}
        for i in link_hb:
            weight[i]=healthy_before[0][i]
        weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
        for i in range(0,len(weight_sort),1):
            weight_sort.pop()
            if len(weight_sort)==fix:
                break
            else:
                continue    
        link_hb=[]
        for i in range(0,len(weight_sort),1):
            link_hb.append(weight_sort[i][0])

    if len(link_ha)!=fix:
        weight={}
        for i in link_ha:
            weight[i]=healthy_after[0][i]
        weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
        for i in range(0,len(weight_sort),1):
            weight_sort.pop()
            if len(weight_sort)==fix:
                break
            else:
                continue    
        link_ha=[]
        for i in range(0,len(weight_sort),1):
            link_ha.append(weight_sort[i][0])

    if len(link_gb)!=fix:
        weight={}
        for i in link_gb:
            weight[i]=GDM_before[0][i]
        weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
        for i in range(0,len(weight_sort),1):
            weight_sort.pop()
            if len(weight_sort)==fix:
                break
            else:
                continue    
        link_gb=[]
        for i in range(0,len(weight_sort),1):
            link_gb.append(weight_sort[i][0])

    link_ha_drop_new={}
    for k in link_ha_drop.keys():
        each=link_ha_drop[k]
        if len(each)!=fix:
            weight={}
            for i in each:
                weight[i]=healthy_after_drop[k][0][i]
            weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
            for i in range(0,len(weight_sort),1):
                weight_sort.pop()
                if len(weight_sort)==fix:
                    break
                else:
                    continue    
            each=[]
            for i in range(0,len(weight_sort),1):
                each.append(weight_sort[i][0])
        link_ha_drop_new[k]=each
    link_ha_drop=link_ha_drop_new
        
    link_gb_drop_new={}
    for k in link_gb_drop.keys():
        each=link_gb_drop[k]
        if len(each)!=fix:
            weight={}
            for i in each:
                weight[i]=GDM_before_drop[k][0][i]
            weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
            for i in range(0,len(weight_sort),1):
                weight_sort.pop()
                if len(weight_sort)==fix:
                    break
                else:
                    continue    
            each=[]
            for i in range(0,len(weight_sort),1):
                each.append(weight_sort[i][0])
        link_gb_drop_new[k]=each
    link_gb_drop=link_gb_drop_new
    
    link_ga_drop_new={}
    for k in link_ga_drop.keys():
        each=link_ga_drop[k]
        if len(each)!=fix:
            weight={}
            for i in each:
                weight[i]=GDM_after_drop[k][0][i]
            weight_sort = sorted(weight.items(), key=lambda d:d[1], reverse = True)
            for i in range(0,len(weight_sort),1):
                weight_sort.pop()
                if len(weight_sort)==fix:
                    break
                else:
                    continue    
            each=[]
            for i in range(0,len(weight_sort),1):
                each.append(weight_sort[i][0])
        link_ga_drop_new[k]=each
    link_ga_drop=link_ga_drop_new
    
    #######2. cross comparsion#####
    ####real#######
    J_cross={}
    ###GBHB
    J_cross['GBHB']={}
    for ii in link_gb_drop.keys():
        each=link_gb_drop[ii]
        count=0
        for jj in each:
            if jj in link_hb:
                count+=1
        J_cross['GBHB'][ii]=count/(len(each)+len(link_hb)-count)
    print('GBHB',np.mean(list(J_cross['GBHB'].values())))
    ###GAHB
    J_cross['GAHB']={}
    for ii in link_ga_drop.keys():
        each=link_ga_drop[ii]
        count=0
        for jj in each:
            if jj in link_hb:
                count+=1
        J_cross['GAHB'][ii]=count/(len(each)+len(link_hb)-count)
    print('GAHB',np.mean(list(J_cross['GAHB'].values())))
    ###GBHA
    J_cross['GBHA']={}
    for ii in link_gb_drop.keys():
        each=link_gb_drop[ii]
        count=0
        for jj in each:
            if jj in link_ha:
                count+=1
        J_cross['GBHA'][ii]=count/(len(each)+len(link_ha)-count)
    print('GBHA',np.mean(list(J_cross['GBHA'].values())))
    ###GAHA
    J_cross['GAHA']={}
    for ii in link_ga_drop.keys():
        each=link_ga_drop[ii]
        count=0
        for jj in each:
            if jj in link_ha:
                count+=1
        J_cross['GAHA'][ii]=count/(len(each)+len(link_ha)-count)
    print('GAHA',np.mean(list(J_cross['GAHA'].values())))
    
    ####shuffle#######
    print('shuffle')
    J_cross_shuffle={}
    ###GBHB
    J_cross_shuffle['GBHB']={}
    for ii in link_gb_drop.keys():
        each_real=link_gb_drop[ii]
        each=list(random.sample(alllink_name,len(each_real)))
        each=[str(t) for t in each]
        count=0
        for jj in each:
            if jj in link_hb:
                count+=1
        J_cross_shuffle['GBHB'][ii]=count/(len(each)+len(link_hb)-count)
    print('GBHB',np.mean(list(J_cross_shuffle['GBHB'].values())))
    ###GAHB
    J_cross_shuffle['GAHB']={}
    for ii in link_ga_drop.keys():
        each_real=link_ga_drop[ii]
        each=list(random.sample(alllink_name,len(each_real)))
        each=[str(t) for t in each]
        count=0
        for jj in each:
            if jj in link_hb:
                count+=1
        J_cross_shuffle['GAHB'][ii]=count/(len(each)+len(link_hb)-count)
    print('GAHB',np.mean(list(J_cross_shuffle['GAHB'].values())))
    ###GBHA
    J_cross_shuffle['GBHA']={}
    for ii in link_gb_drop.keys():
        each_real=link_gb_drop[ii]
        each=list(random.sample(alllink_name,len(each_real)))
        each=[str(t) for t in each]
        count=0
        for jj in each:
            if jj in link_ha:
                count+=1
        J_cross_shuffle['GBHA'][ii]=count/(len(each)+len(link_ha)-count)
    print('GBHA',np.mean(list(J_cross_shuffle['GBHA'].values())))
    ###GAHA
    J_cross_shuffle['GAHA']={}
    for ii in link_ga_drop.keys():
        each_real=link_ga_drop[ii]
        each=list(random.sample(alllink_name,len(each_real)))
        each=[str(t) for t in each]
        count=0
        for jj in each:
            if jj in link_ha:
                count+=1
        J_cross_shuffle['GAHA'][ii]=count/(len(each)+len(link_ha)-count)
    print('GAHA',np.mean(list(J_cross_shuffle['GAHA'].values())))

    GBHB_mean.append(np.mean(list(J_cross['GBHB'].values())))
    GBHA_mean.append(np.mean(list(J_cross['GBHA'].values())))
    GAHB_mean.append(np.mean(list(J_cross['GAHB'].values())))
    GAHA_mean.append(np.mean(list(J_cross['GAHA'].values())))
    GBHB_shuffle_mean.append(np.mean(list(J_cross_shuffle['GBHB'].values())))
    GBHA_shuffle_mean.append(np.mean(list(J_cross_shuffle['GBHA'].values())))
    GAHB_shuffle_mean.append(np.mean(list(J_cross_shuffle['GAHB'].values())))
    GAHA_shuffle_mean.append(np.mean(list(J_cross_shuffle['GAHA'].values())))
    GBHB_std.append(np.std(list(J_cross['GBHB'].values()),ddof=1))
    GBHA_std.append(np.std(list(J_cross['GBHA'].values()),ddof=1))
    GAHB_std.append(np.std(list(J_cross['GAHB'].values()),ddof=1))
    GAHA_std.append(np.std(list(J_cross['GAHA'].values()),ddof=1))
    GBHB_shuffle_std.append(np.std(list(J_cross_shuffle['GBHB'].values()),ddof=1))
    GBHA_shuffle_std.append(np.std(list(J_cross_shuffle['GBHA'].values()),ddof=1))
    GAHB_shuffle_std.append(np.std(list(J_cross_shuffle['GAHB'].values()),ddof=1))
    GAHA_shuffle_std.append(np.std(list(J_cross_shuffle['GAHA'].values()),ddof=1))

plt.errorbar(X,GBHB_mean,yerr=GBHB_std,fmt="bo:",label='H(W0)-G(H0)')
plt.errorbar(X,GAHB_mean,yerr=GAHB_std,fmt="b^:",label='H(W0)-G(H2)')
plt.errorbar(X,GBHA_mean,yerr=GBHA_std,fmt="ro:",label='H(W2)-G(H0)')
plt.errorbar(X,GAHA_mean,yerr=GAHA_std,fmt="r^:",label='H(W2)-G(H2)')
plt.errorbar(X,GBHB_shuffle_mean,yerr=GBHB_shuffle_std,fmt="go:",label='H(W0)-G(H0)_shuffle')
plt.errorbar(X,GAHB_shuffle_mean,yerr=GAHB_shuffle_std,fmt="g^:",label='H(W0)-G(H2)_shuffle')
plt.errorbar(X,GBHA_shuffle_mean,yerr=GBHA_shuffle_std,fmt="ko:",label='H(W2)-G(H0)_shuffle')
plt.errorbar(X,GAHA_shuffle_mean,yerr=GAHA_shuffle_std,fmt="k^:",label='H(W2)-G(H2)_shuffle')
plt.legend()
plt.xlabel('W')
plt.xlim(0.9,3.7,0.1)
plt.ylabel('Jaccard similarity')
plt.grid()
plt.show()
plt.close()    


########################F3############################
for fix in range(100,1200,200):
    #######HB#########
    if len(healthy_before)>fix:
        healthy_before_sort =  healthy_before.sort_values(by=0,ascending=False)
        healthy_before_top =  healthy_before_sort[0:fix]
    #######HA#########
    if len(healthy_after)>fix:
        healthy_after_sort =  healthy_after.sort_values(by=0,ascending=False)
        healthy_after_top =  healthy_after_sort[0:fix]
    #######GB#########
    if len(GDM_before)>fix:
        GDM_before_sort =  GDM_before.sort_values(by=0,ascending=False)
        GDM_before_top =  GDM_before_sort[0:fix]
    #######GA#########
    if len(GDM_after)>fix:
        GDM_after_sort =  GDM_after.sort_values(by=0,ascending=False)
        GDM_after_top =  GDM_after_sort[0:fix]
    ########HA drop###########
    healthy_after_drop_top={}
    for k in healthy_after_drop.keys():
        each=healthy_after_drop[k]
        if len(each)>fix:
            each_sort = each.sort_values(by=0,ascending=False)
            each_500 =  each_sort[0:fix]
        healthy_after_drop_top[k]=each_500
    ########GB drop###########
    GDM_before_drop_top={}
    for k in GDM_before_drop.keys():
        each=GDM_before_drop[k]
        if len(each)>fix:
            each_sort = each.sort_values(by=0,ascending=False)
            each_500 =  each_sort[0:fix]
        GDM_before_drop_top[k]=each_500
    ########GA drop###########
    GDM_after_drop_top={}
    for k in GDM_after_drop.keys():
        each=GDM_after_drop[k]
        if len(each)>fix:
            each_sort = each.sort_values(by=0,ascending=False)
            each_500 =  each_sort[0:fix]
        GDM_after_drop_top[k]=each_500
    
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
    plt.title('fix top %d links'%(fix))
    plt.show()
    plt.close()




