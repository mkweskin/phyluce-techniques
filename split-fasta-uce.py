#! /usr/bin/env python3

import argparse
from Bio import SeqIO
import re

def get_args():
    parser = argparse.ArgumentParser(description="""Takes a large alignment and splits into seperate files, one for each uce.""")
    parser.add_argument(
        'fasta',
        type=str,
        help="""FASTA file to read in"""
    )
    return parser.parse_args()


def main():
    args = get_args()

    for seq_record in SeqIO.parse(args.fasta, "fasta"):
        uce_id = re.findall("\|(uce-.*)", seq_record.description)
        if len(uce_id[0]) > 4:
            with open(uce_id[0]+".fasta", "a") as output_handle:
                SeqIO.write(seq_record, output_handle, "fasta")

if __name__ == '__main__':
    main()
