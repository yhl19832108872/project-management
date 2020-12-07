# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 11:53:45 2020

@author: Samsung-PC
"""


import difflib
import numpy as np
from Bio.SeqUtils import GC
from Bio import pairwise2
from Bio.Seq import Seq 

import re




def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def score(seq1,seq2):
    seq1=Seq(seq1)
    seq2=Seq(seq2)
    alignments = pairwise2.align.globalxx(seq1,seq2)
    return alignments[0].score


def get_index_list(filename,seq_number):
    
    with open(filename,'r') as f:
        data=f.read()
    all_information=re.search(seq_number+'(.*?)//',str(data),re.S).group()
    gene_formation=re.search('.*ORIGIN',all_information,re.S).group()
    seq_information=re.findall('ORIGIN(.*?)//',all_information,re.S)[0]
    write_seq(seq_information)
    

        
    index_ori_list=re.findall('gene (.*)\n',gene_formation)
    index_list=[]
    for index in index_ori_list:   
        index_list.append(re.findall(r'\d+',index))
    index_list=np.array(index_list,dtype=int)
 
    #判断ATP8是否已经标注
    atp8_exist=gene_formation.find('ATP8')
    if atp8_exist!=-1:
        #如果ATP8已经标注出，将ATP8的在链上的索引去除
        atp8_index=re.findall('gene\s+<?\d+\.\..?\d+\n.*?=(.*?)\n',gene_formation).index('"ATP8"')
#        gene_formation=gene_formation[:atp8_exist-58]+gene_formation[atp8_exist:]
#        index_list=np.vstack((index_list[:atp8_index,:],index_list[atp8_index+1:,:]))

        a=index_list[:atp8_index,:]
        b=index_list[atp8_index+1:,:]

        index_list=np.vstack((a,b))
#        print(index_list)
    return index_list

def get_seq(filename):
    
    with open(filename,'r') as f:
        lines =f.readlines()
    seq=''
    
    for line in lines:
        line=line.strip()
        temp=line.split(' ')
        temp.pop(0)
        line=''.join(temp)
        seq+=line
    return seq

def get_pro_atp8(seq,starts,ends,ref_index_list,Reading_box=0):
    start_indexs=[]
    end_indexs=[]
    
    for i in range(Reading_box,len(seq),3):
        if seq[i:i+3] in starts:
            Flag=True
            for indexs in ref_index_list:
                if indexs[0]<i<indexs[1]:
                    Flag=False
                    break
            if Flag==True:
                start_indexs.append(i)
        if seq[i:i+3] in ends:
            Flag=True
            for indexs in ref_index_list:
                if indexs[0]<i<indexs[1]:
                    Flag=False
                    break
            if Flag==True:
                end_indexs.append(i+3)
        
    
    probable_atp8=[]
    for i in start_indexs:
        for j in end_indexs:
            if 100<j-i<170:
                Flag=True

                for indexs in ref_index_list:
                    if i+1<indexs[0]<j+1:
                        Flag=False
                        break
                for indexs in ref_index_list:
                    if i+1<indexs[1]<j+1:
                        Flag=False
                        break
                if Flag==True:
                    probable_atp8.append(seq[i:j])
    return probable_atp8


def write_seq(ori_seq):
    with open("seq.txt","w") as f:
        f.write(ori_seq) 


def main(seq_number):

    # seq_number=g.enterbox(msg="请输入基因序列号",title="查找ATP8接口")
    index_list=get_index_list('data.txt',seq_number)
    seq=get_seq('seq.txt')
    starts=['ata','atg','att','gtg']
    ends=['taa','tag']
    reverse_complement_seq=str(Seq(seq).reverse_complement())
    ref_index_list_p=np.zeros(index_list.shape)
    for i in range(len(index_list)):
        ref_index_list_p[i][0]=index_list[i][0]+5
        ref_index_list_p[i][1]=index_list[i][1]-5
    
    index_list_n=np.array(index_list)
    for i in range(len(index_list_n)):
        for j in range(len(index_list_n[i])):
            index_list_n[i][j]=len(seq)-index_list_n[i][j]+1
    ref_index_list_n=np.zeros(index_list.shape)
    for i in range(len(index_list)):
        ref_index_list_n[i][0]=index_list_n[i][0]+5
        ref_index_list_n[i][1]=index_list_n[i][1]-5
    
    references=['ataccacaattgtcaaggtttgggatttttagtttttatttagttattatttcatctttgattttattatcaattgttattttgagttttgttttttctaatcgtgttgatcaagtttatttcgaaaattcttctttttctgggggggttagttttttttgattttaa',
            'atgccccagttaggaaaattgcctgttgtttttattttcgttttggtgggtttagtttttagtgttttaatgattgaagtttatgggagcccctggtttgggggtgagagggaattaagggggggtttaagggggaggggcgtggagcatccttgaaaaatttaa',
           'atgcctcatatagcacctatttactgggctttggtatgtttgcttgtttggttttgaatgttagttatgttttctaagcgatgatttgggggctttgttgtttccttcaaagtttag',
           'ataatgcctcatataagcccaataaattgaatttatttcctatgcattacactattttttattatttcatttaccaaaaatttttcctcttcttcaccatcagttacacctaattttcaaattattaaaaacaaaagtaaaataaaaatttttaaaaccaaatgataa',
           'attaagttgcctcatatgagtcctataaattgactgtattttatatttatttttttttgtattatgttctcttttttatttttttttgattctaataataaagataatgatagaatattgcattttgtttctttaaaaaaaagtaattttaaatgataa',
            'atgccgcattttagagatatttatgttatagtattatttgttattagaataattgtagttgtatgttttttagtgttgctttgatgaactaggaaaatggaaagtcttgacccggaagaagtggaaaattggattttaattt',
            'attccacaaatagcacctattagatgattattattatttattattttttctattacatttattttattttgttctattaactattattcttatataccaaattcacctaaatctaatgaattaaaaaatatcaacttaaattcaataaattgaaaatgataa',
            'atgccacaattagttccattttattttatgaatcaattaacatatggtttcttattaatgattctattattaattttattctcacaattctttttacctatgatcttaagattatatgtatctagattatttatttctaaattataa'
           ]
    
    

    probable_atp8_p=[]
    for i in range(3):
        probable_atp8_p.extend(get_pro_atp8(seq,starts,ends,ref_index_list_p,i))
    
    
    probable_atp8_n=[]
    for i in range(3):
        probable_atp8_n.extend(get_pro_atp8(reverse_complement_seq,starts,ends,ref_index_list_n,i))
                
    
   

    GC_content=[]
    for reference in references:
        GC_content.append(1/GC(reference))
    total=sum(GC_content)
    GC_weights=[]
    for gc in GC_content:
        GC_weights.append(gc/total)
    
    similiars_p=[]
    for atp8 in probable_atp8_p:
        similiar=0
        i=0
        for reference in references:
            similiar+=score(atp8,reference)*GC_weights[i]
            i+=1
            
        similiars_p.append(similiar)
    
    similiars_n=[]
    for atp8 in probable_atp8_n:
        similiar=0
        i=0
        for reference in references:
            similiar+=score(atp8,reference)*GC_weights[i]
            i+=1
        similiars_n.append(similiar)
    
    
    atp8_p=probable_atp8_p[similiars_p.index(max(similiars_p))]
    atp8_p_start=seq.find(atp8_p)
    atp8_p_end=atp8_p_start+len(atp8_p)

    
    
    atp8_n=probable_atp8_n[similiars_n.index(max(similiars_n))]
    reverse_complement=str(Seq(atp8_n).reverse_complement())
    atp8_n_start=seq.find(reverse_complement)
    atp8_n_end=atp8_n_start+len(atp8_n)

    
    if max(similiars_p)>max(similiars_n):
        print("atp8 on +  :",atp8_p)
        print("the atp8 index is :%d-%d"%(atp8_p_start+1,atp8_p_end))
        return atp8_p
    else:
        print("atp8 on -  :",atp8_n)
        print("the atp8 index is :%d-%d"%(atp8_n_start+1,atp8_n_end))
        return atp8_n
    
    


  




