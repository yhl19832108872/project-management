from Bio import SeqIO

def format_fasta(ana, seq):
    """
    格式化文本为 fasta格式
    ana: 注释信息
    seq: 序列
    return: fasta格式文本
    """
    format_seq = ""
    for i in seq:
        format_seq += i
    return ana + '\n' + format_seq + "\n"

def get_cds(gb_file, cds_gene):
    '''
    找出某编码蛋白的索引
    gb_file: genbank文件
    cds_gene: 某蛋白质
    返回基因索引值, 注释 和 基因序列
    '''
    cds_id = gb_file.id
    cds_description = gb_file.description
    for i in gb_file.features:
        if i.type == 'CDS':
            if ('gene' in i.qualifiers.keys()):
                if cds_gene == i.qualifiers['gene'][0]:
                    start = i.location.start
                    end = i.location.end
                    seq = gb_file.seq[start:end]
                    ana = ">" + cds_id + ":" + str(start) + "-" + str(end) + " " + cds_description
                    return start, end, ana, seq
                else:
                    continue

# # 读取genbank文件
# path = "F:/mito_annotation/含ATP8的序列/直口涡虫_NC_035256.gb"
# gb_seq = SeqIO.read(path, "genbank")
# start, end, ana, seq = get_cds(gb_seq, "ATP8")
# # 找到的基因格式化为fasta
# cds_file_obj = open('NC_050391.fasta', "w")
# cds_fasta = format_fasta(ana, seq)
# cds_file_obj.write(cds_fasta)
# cds_file_obj.close()