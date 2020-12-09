from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram
from Bio.SeqFeature import SeqFeature, FeatureLocation

def visualize(record, atp8_start, atp8_end, strand):
    gd_diagram = GenomeDiagram.Diagram("Mitochondrion")
    gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
    gd_feature_set = gd_track_for_features.new_set()
    
    atp8_feature = SeqFeature(location=FeatureLocation(atp8_start,atp8_end), strand=strand, type='gene', qualifiers={'gene': [ 'ATP8' ]})
    gd_feature_set.add_feature(atp8_feature, color=colors.lightblue, label=True, label_position='middle')
    
    for feature in record.features:
        if feature.type == 'CDS':
            color = colors.lightblue
        elif feature.type == 'tRNA':
            color = colors.HexColor("#FF8100")
        elif feature.type == 'rRNA':
            color = colors.lightgreen
        else:
            continue
        gd_feature_set.add_feature(feature, color=color, label=True, label_position='middle')
        
    gd_diagram.draw(format='circular', circular=True, pagesize=(20*cm, 20*cm), start=0, end=len(record), circle_core=0.7)
    gd_diagram.write('.\\static\\people_photo\\visualize.png', "PNG")
    
def visualize2(record):
    gd_diagram = GenomeDiagram.Diagram("Mitochondrion")
    gd_track_for_features = gd_diagram.new_track(1, name="Annotated Features")
    gd_feature_set = gd_track_for_features.new_set()
    for feature in record.features:
        if feature.type == 'CDS':
            color = colors.lightblue
        elif feature.type == 'tRNA':
            color = colors.HexColor("#FF8100")
        elif feature.type == 'rRNA':
            color = colors.lightgreen
        else:
            continue
        gd_feature_set.add_feature(feature, color=color, label=True, label_position='middle')
        
    gd_diagram.draw(format='circular', circular=True, pagesize=(20*cm, 20*cm), start=0, end=len(record), circle_core=0.7)
    gd_diagram.write('.\\static\\visualize.pdf', "PDF")
    
    