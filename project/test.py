# # -*- coding: utf-8 -*-
# """
# Created on Sun Dec 13 14:35:36 2020
#
# @author: zhangxiu
# """
#
# from Bio import pairwise2, SeqIO
# import csv
# # import process
# # from Bio.Seq import Seq
# # seq1 = Seq('ATGCCCCAACTAAATACCGCCGTATGACCCACCATAATTACCCCCATACTCCTGACACTATTTCTCGTCACCCAACTAAAAATATTAAATTCAAATTACCATCTACCCCCCTCACCAAAACCCATAAAAATAAAAAACTACAATAAACCCTGAGAACCAAAATGAACGAAAATCTATTCGCTTCATTCGCTGCCCCCACAATCCTAG')
# # seq2 = Seq('ATGCCCCAACTAAATACTACTGTATGGCCCACCATAATTATCCCCATACTCCTTACACTATTCCTCATCACCCAACTAAAAATATTAAATACAAATTACCACTTACCTCCCTCACCAAAGCCCATAAAAATAAAAAACTATAACAAACCCTGAGAACCAAAATGAACGAAAATCTGTTCGCTTCATTCATTGCCCCCACAATCCTAG')
# # alignments = pairwise2.align.globalxx(seq1, seq2)
# # score = alignments[0].score
# # acc = (score / alignments[0].end) * 100
# # print(score, acc)
#
# records = SeqIO.parse('predict4(1)(acc).fa', 'fasta')
# records = list(records)
# header = ['Seq1ID', 'Seq2ID', 'Score', 'Similarity']
# file = open("result2(acc).csv", "a+", newline="")
# content = csv.writer(file)
# content.writerow(header)
# for i, record in enumerate(records):
#     for record1 in records[1+i:]:
#         alignments = pairwise2.align.globalxx(record.seq, record1.seq)
#         score = alignments[0].score
#         acc = (score / alignments[0].end) * 100
#         print(score, acc)
#         content.writerow([record.id, record1.id, score, acc])
# file.close()
#
# # ids = ['DQ985706', 'NC_039446', 'NC_009463', 'EF420138', 'NC_017613', 'NC_017615', 'NC_039445', 'KJ599679', 'KY114889', 'KY114886']
# # # ids = ['NC_050392']
# # for seqId in ids:
# #     print(seqId, end=':')
# #     process.write_gbk(seqId)
# #     strand, seq, position = process.main(seqId)
# #     print(position)
# #     with open('predict4(1)(acc).txt', 'a+') as f:
# #         f.write('>'+seqId+'\n')
# #         f.write(seq+'\n')
# # alignments = pairwise2.align.globalxx(seq1,seq2)
# # print(alignments[0].score)
#
#