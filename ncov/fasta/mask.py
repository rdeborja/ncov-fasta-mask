'''

'''

import re
import csv
from Bio import SeqIO


def import_bed_file(bed):
    '''
    Import a BED file containing regions and return a matrix containing those
    regions.
    '''
    primers = []
    with open(bed, 'r') as bed_f:
        for line in bed_f:
            line = line.rstrip()
            tmp_data = line.split(sep='\t')
            primers.append(tmp_data)
    return primers


def mask_region():
    '''
    Mask a region provided as arguments with a replacement base (default: N).
    '''
    pass


def import_fasta():
    '''
    Import a FASTA file for processing.  The function returns a Bio.SeqIO
    object.
    '''
    pass


def get_primer_pool(primers, pattern):
    '''
    Get the primers associated with a pool given a provided pattern.
    '''
    primers_pool = []
    for primer in primers:
        if re.search(pattern, primer[4]):
            primers_pool.append(primer)
    return primers_pool
