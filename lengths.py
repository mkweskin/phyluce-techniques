#!/usr/bin/env python3

import argparse
from Bio import SeqIO
import re
import os

def get_args():
    parser = argparse.ArgumentParser(description="""Returns sequences containing less than a certain proportion nucleotides compared to alignment length""")
    parser.add_argument(
        'alignment',
        type=str,
        help="""Alignment file to examine"""
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=["fasta","fastq","phylip","nexus","clustalw"],
        default="fasta",
        help="""Input format of the alignment (fasta, fastq, phylip, nexus, clustalw). Default: fasta"""
    )
    parser.add_argument(
        '--prop',
        type=float,
        default=".1",
        help="""Minimum proportion of sites present in sequence to trigger alert. Default: 0.1"""
    )
    parser.add_argument(
        '--min-length',
        type=int,
        default="0",
        help="""Minimum length of sequence. If specified, this is used in addition to proportion. Default: not used, only proportion is used"""
    )
    parser.add_argument(
        '--include-zero',
        default=False,
        action='store_true',
        help="""Show sequences that have zero lenght. Default: False"""
    )
    parser.add_argument(
        '--remove',
        default=False,
        action='store_true',
        help="""Remove the identified short sequences from the alignment, make a new alignment file prefixed with \"reduced_\". Output format is always fasta. Default: False"""
    )
    parser.add_argument(
        '--protein',
        default=False,
        action='store_true',
        help="""The input alignment are proteins. Default: False"""
    )
    return parser.parse_args()

def main():
    args = get_args()
    good_seqs = []

    seqs = list(SeqIO.parse(args.alignment, args.format))
    for seq_record in seqs:
        if args.protein:
            goodlen = len(re.findall("[arndbceqzghilkmfpstwyv]", str(seq_record.seq).lower()))
        else:
            goodlen = len(re.findall("[acgt]", str(seq_record.seq).lower()))
        if (goodlen / len(seq_record.seq) < args.prop and goodlen != 0) or (args.min_length > 0 and goodlen < args.min_length and goodlen != 0) or (goodlen == 0 and args.include_zero):

            print (args.alignment + "	" + seq_record.id + "	" + str(goodlen))
        else:
            good_seqs.append(seq_record.id)

    if args.remove:
        os.system ("rm -f reduced_" + args.alignment + ".fasta")
        for seq_record in seqs:
            if seq_record.id in good_seqs:
                with open( "reduced_" + args.alignment + ".fasta", "a") as output_handle:
                    SeqIO.write(seq_record, output_handle, "fasta")

if __name__ == '__main__':
    main()

