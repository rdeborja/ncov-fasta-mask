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
parser.add_argument('-p', '--pool',
                    help='amplicon ID pattern for pool of interest')
parser.add_argument('-o', '--output', help='filename to write new FASTA to',
                    default="output.fasta")

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

primers = mask.import_bed_file(bed=args.bed)
pool = mask.get_primer_pool(primers=primers, pattern=args.pool)
primer_pairs = mask.create_primer_pairs(primers=pool)
masked_fasta = mask.mask_fasta_with_regions(fasta=args.fasta, regions=primer_pairs)

with open(args.output, 'w') as fasta_o:
    for line in masked_fasta:
        fasta_o.write(line + '\n')
