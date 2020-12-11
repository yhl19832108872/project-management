# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 14:43:28 2020

@author: zhangxiu
"""
from Bio import SeqIO

filename = 'gene_information.gbk'
record = SeqIO.read(filename, 'genbank')
index_list=[]

for feature in record.features:
    if feature.type == 'gene':
        location = feature.location
        index_list.append([location.start, location.end])
print(index_list)