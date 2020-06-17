'''

'''

import re
import csv
import json
import textwrap as tw
from Bio import SeqIO


def import_bed_file(bed):
    '''
    Import a BED file containing regions and return a matrix containing those
    regions.

    Arguments:
        * bed: full path to a BED file to process

    Return Value:
        Returns a list of primers from the BED file
    '''
    primers = []
    with open(bed, 'r') as bed_f:
        for line in bed_f:
            line = line.rstrip()
            tmp_data = line.split(sep='\t')
            primers.append(tmp_data)
    return primers


def create_masked_sequence(start, end, replace):
    '''

    '''
    replace_length = end - start + 1
    return replace_length * replace


def mask_fasta_with_regions(fasta, regions, start='left_start', end='right_end', replace='N'):
    '''
    Mask a region provided as arguments with a replacement base (default: N).

    Arguments:
        * fasta:    FASTA file to process
        * regions:  a dictionary containing regions to mask
        * start:    key name for the start of the region
        * end:      key name for the end of the region
        * replace:  the character to replace nulcleotides with (default: N)
    
    Return Value:
        Returns a FASTA sequence with the masked regions
    '''
    masked_sequence = ''
    header = ''
    fasta_record = []
    with open(fasta, 'r') as fasta_p:
        for record in SeqIO.parse(fasta_p, 'fasta'):
            header = ''.join(['>', str(record.id)])
            fasta_record.append(header)
            masked_sequence = str(record.seq)
            for region in regions:
                if all (k in regions[region] for k in (start, end)):
                    replace_range = regions[region][end] - regions[region][start] + 1
                    replace_seq = replace_range * replace
                    start_seq = regions[region][start] - 1
                    end_seq = regions[region][end] + 1
                    masked_sequence = masked_sequence[:start_seq] + replace_seq + masked_sequence[end_seq:]
    return fasta_record + tw.wrap(masked_sequence, width=60)


def get_primer_pool(primers, pattern):
    '''
    Get the primers associated with a pool given a provided pattern.

    Arguments:
        * primers:  a list containing a list of primers
        * pattern:  the pattern to search that indicates the pool association
                    in the primer name

    Return Value:
        Returns a list of primers associated with a specific pool
    '''
    primers_pool = []
    for primer in primers:
        if re.search(pattern, primer[4]):
            primers_pool.append(primer)
    return primers_pool


def create_primer_pairs(primers, left='_LEFT', right='_RIGHT'):
    '''
    From a list of primers, create a dictionary containing the left and right
    regions in a single entry.

    Arguments:
        * primers:  a list containing primers to process
        * left:     string pattern for the left primer in the id
        * right:    string pattern for the right primer in the id

    Return Value:
        Returns a dictionary with the primer ID as key and the following:
            * left_start:       start position of the left primer
            * left_end:         end position of the left primer
            * right_start:      start position of the right primer
            * right_end:        end position of the right primer
    '''
    primer_pairs = {}
    tmp_primer = {}
    pattern = ''.join(["(", left, '|', right, ")"])
    for primer in primers:
        primer_id = re.sub(pattern, '', primer[3])
        if primer_id not in primer_pairs.keys():
            primer_pairs[primer_id] = {}
        if re.search(left, primer[3]):
            primer_pairs[primer_id]['left_start'] = int(primer[1])
            primer_pairs[primer_id]['left_end'] = int(primer[2])
        elif re.search(right, primer[3]):
            primer_pairs[primer_id]['right_start'] = int(primer[1])
            primer_pairs[primer_id]['right_end'] = int(primer[2])
        else:
            print('skipping')
            print(primer)
    return primer_pairs