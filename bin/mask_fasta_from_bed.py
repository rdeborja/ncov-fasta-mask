#!/usr/bin/env python
'''
Mask regions of a FASTA file with N based on a BED file containing regions to
convert.
'''

import sys
import argparse
import os
import re
import ncov.fasta.mask as mask
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fasta', help='FASTA file to process')
parser.add_argument('-b', '--bed', help='BED file containing regions to mask')
parser.add_argument('-o', '--output', help='filename to write new FASTA to',
                    default="output.fasta")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

pool1 = []
pool2 = []
primers = mask.import_bed_file(bed=args.bed)
for primer in primers:
    if re.search('_1$', primer[4]):
        pool1.append(primer)
    elif re.search('_2$', primer[4]):
        pool2.append(primer)

with open(args.fasta, 'r') as fasta_p:
    for record in SeqIO.parse(fasta_p, 'fasta'):
        mask_seq = str(record.seq)
        for primer in pool1:
            print(mask_seq[int(primer[1]):int(primer[2])])