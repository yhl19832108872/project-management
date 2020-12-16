import numpy as np
from Bio.SeqUtils import GC
from Bio import pairwise2, SeqIO
import os
import re
from visualization import visualize1, visualize2

def score(seq1,seq2):
    alignments = pairwise2.align.globalxx(seq1,seq2)
    return (alignments[0].score / alignments[0].end) * 100
    # return alignments[0].score

def write_gbk(seq_number):
    filename = 'MitoGenPlatyhelminthes.gbk'
    with open(filename,'r') as f:
        data=f.read()
    information=re.search('LOCUS       '+seq_number+'(.*?)//',str(data),re.S).group()
    with open('uploads\\gene_information.gbk','w') as f:
        f.write(information)

def get_index_list(record):
    seq = record.seq
    index_list=[]
    for feature in record.features:
        if feature.type == 'gene':
            location = feature.location
            index_list.append([location.start, location.end])
    index_list = np.array(index_list, dtype=int)
    
    return seq, index_list

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
                atp8=seq[i:j]
                Flag=True

                for indexs in ref_index_list:
                    if i < indexs[0] < j:
                        Flag=False
                        break
                for indexs in ref_index_list:
                    if i < indexs[1]< j:
                        Flag=False
                        break
                for k in range(0,len(atp8)-3,3):
                    for end in ends:
                        if end==atp8[k:k+3]:
                            Flag=False
                
                if Flag==True:
                    probable_atp8.append(seq[i:j])
    return probable_atp8

def main():
    # filename = os.path.join('datasets', seqId+'.gbk')
    filename = os.path.join('uploads\\gene_information.gbk')
    record = SeqIO.read(filename, 'genbank')
    # 判断ATP8是否已经标注
    for feature in record.features:
        if feature.type == 'gene':
            location = feature.location
            start = location.start
            end = location.end
            if feature.qualifiers.get('gene'):
                if 'ATP8' in feature.qualifiers['gene']:
                    atp8 = record.seq[start:end]
                    strand = feature.strand
                    flag = '+' if strand == 1 else '-'
                    visualize2(record)
                    return "ATP8 on "+flag+"  :", str(atp8), 'The ATP8 index is :'+str(start+1)+'-'+str(end)
    # 获得非编码基因
    seq, index_list = get_index_list(record)
    starts=['ATA','ATG','ATT','GTG']
    ends=['TAA','TAG']
    reverse_complement_seq=seq.reverse_complement()
    ref_index_list_p=np.zeros(index_list.shape)
    for i in range(len(index_list)):
        ref_index_list_p[i][0]=index_list[i][0]+5
        ref_index_list_p[i][1]=index_list[i][1]-5
    
    ref_index_list_n=np.zeros(index_list.shape)
    for i in range(len(index_list)):
        ref_index_list_n[i][0] = len(seq)-1-index_list[i][1]+5
        ref_index_list_n[i][1] = len(seq)-1-index_list[i][0]-5
    
    # index_list_n=np.array(index_list)
    # for i in range(len(index_list_n)):
    #     for j in range(len(index_list_n[i])):
    #         index_list_n[i][j]=len(seq)-index_list_n[i][j]-1
    # ref_index_list_n=np.zeros(index_list.shape)
    # for i in range(len(index_list)):
    #     ref_index_list_n[i][0]=index_list_n[i][0]+5
    #     ref_index_list_n[i][1]=index_list_n[i][1]-5
    
    # 读取参考序列
    references = SeqIO.parse('reference.fa', 'fasta')
    references = list(references)
    
    # 计算参考序列权重
    GC_content=[]
    for reference in references:
        GC_content.append(1/GC(reference.seq))
    total=sum(GC_content)
    GC_weights=[]
    for gc in GC_content:
        GC_weights.append(gc/total)
        
    # 从非编码基因的六种阅读框中找到备选ATP8序列
    probable_atp8_p=[]
    for i in range(3):
        probable_atp8_p.extend(get_pro_atp8(seq,starts,ends,ref_index_list_p,i))
    
    probable_atp8_n=[]
    for i in range(3):
        probable_atp8_n.extend(get_pro_atp8(reverse_complement_seq,starts,ends,ref_index_list_n,i))
    
    # 备选序列与参考序列比对 计算得分
    similiars_p=[]
    for atp8 in probable_atp8_p:
        similiar=0
        i=0
        for reference in references:
            similiar+=score(atp8,reference.seq.upper())*GC_weights[i]
            i+=1
        similiars_p.append(similiar)
    
    similiars_n=[]
    for atp8 in probable_atp8_n:
        similiar=0
        i=0
        for reference in references:
            similiar+=score(atp8,reference.seq.upper())*GC_weights[i]
            i+=1
        similiars_n.append(similiar)
        
    sp = sn = 0
    if len(similiars_p) > 0:
        atp8_p=probable_atp8_p[similiars_p.index(max(similiars_p))]
        atp8_p_start=seq.find(atp8_p)
        atp8_p_end=atp8_p_start+len(atp8_p)
        sp = max(similiars_p)
        
    if len(similiars_n) > 0:
        atp8_n=probable_atp8_n[similiars_n.index(max(similiars_n))]
        reverse_complement=atp8_n.reverse_complement()
        atp8_n_start=seq.find(reverse_complement)
        atp8_n_end=atp8_n_start+len(atp8_n)
        sn = max(similiars_n)
    
    if sp > sn:
        strand = 1
        flag = '+'
        atp8 = atp8_p
        atp8_start = atp8_p_start
        atp8_end = atp8_p_end
        max_similiar = sp
    else:
        strand = -1
        flag = '-'
        atp8 = atp8_n
        atp8_start = atp8_n_start
        atp8_end = atp8_n_end
        max_similiar = sn
    print(max_similiar, end=' ')
    visualize1(record, atp8_start, atp8_end, strand)
    return "ATP8 on "+flag+"  :", str(atp8), 'The ATP8 index is :'+str(atp8_start+1)+'-'+str(atp8_end)

    
    
