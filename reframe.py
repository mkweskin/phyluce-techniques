#!/usr/bin/env python3

import argparse
from Bio import SeqIO, AlignIO
import re
import sys
#import os

def get_args():
    parser = argparse.ArgumentParser(description="""Takes a trimmed sequence and compares it to its untrimmed predecessor and makes sure the two are in the same frame. If necessary, 1-2 positions are trimmed form the beginning or end of the sequence.""")
    parser.add_argument(
        'trimmed',
        type=str,
        help="""Trimmed alignment file to which to adjust the frame"""
    )
    parser.add_argument(
        'untrimmed',
        type=str,
        help="""UN-trimmed, original alignment file"""
    )
    parser.add_argument(
        'outfile',
        type=str,
        help="""Name of the output file"""
    )
    parser.add_argument(
        '--informat-trimmed',
        type=str,
        choices=["fasta","fastq","phylip","nexus","clustalw"],
        default="fasta",
        help="""Input format of the trimmed alignment (fasta, fastq, phylip, nexus, clustalw). Default: fasta"""
    )
    parser.add_argument(
        '--informat-untrimmed',
        type=str,
        choices=["fasta","fastq","phylip","nexus","clustalw"],
        default="fasta",
        help="""Input format of the trimmed alignment (fasta, fastq, phylip, nexus, clustalw). Default: fasta"""
    )
    parser.add_argument(
        '--outformat',
        type=str,
        choices=["fasta","fastq","phylip","nexus","clustalw"],
        default="fasta",
        help="""Output format of the alignment (fasta, fastq, phylip, nexus, clustalw). Default: fasta"""
    )
    return parser.parse_args()

def main():
    args = get_args()

    # Read in the two alignment files
    #trimmed_seqs = list(SeqIO.parse(args.trimmed, args.informat_trimmed))
    #untrimmed_seqs = list(SeqIO.parse(args.untrimmed, args.informat_untrimmed))

    trimmed_seqs = AlignIO.read(args.trimmed, args.informat_trimmed)
    untrimmed_seqs = AlignIO.read(args.untrimmed, args.informat_untrimmed)


    # Get the first sequence, clean up (lower and change ? to -) and find trimmed in untrimmed
    trimmed_seq = str(trimmed_seqs[0].seq).lower().replace("?", "-")
    untrimmed_seq = str(untrimmed_seqs[0].seq).lower().replace("?", "-")

    # For the trimmed sequence, remove any left or right gaps, otherwise the trimmed may not be found in the untrimmed.
    # Need to keep track of how gaps are at beginning (left) and end (right)
    trimmed_seq_no_left_gaps = re.sub ("^-+", "", trimmed_seq)
    trimmed_left_gaps = len(trimmed_seq) - len(trimmed_seq_no_left_gaps)

    trimmed_seq_no_left_no_right_gaps = re.sub ("-+$", "", trimmed_seq_no_left_gaps)
    trimmed_right_gaps = len(trimmed_seq_no_left_gaps) - len(trimmed_seq_no_left_no_right_gaps)

    # Find the trimmed in the untrimmed
    start = None
    end = None
    for m in re.finditer(trimmed_seq_no_left_no_right_gaps, untrimmed_seq):
        start = m.start()
        end = m.end()

    if (start == None or end == None):
        print ("ERROR: the trimmed sequence was not found in the untrimmed sequence.")
        sys.exit()


    # Add back the removed gaps from beginning/end
    start -= trimmed_left_gaps
    end += trimmed_right_gaps

    # Adjust start to maintain frame with untrimmed
    start_adj = 0
    start_mod = start % 3
    if start_mod == 1:
        start_adj = 2
    elif start_mod == 2:
        start_adj = 1

    # Adjust end to end on a full codon
    end_adj = 0
    end_mod = end % 3
    if end_mod == 1:
        end_adj = 1
    elif end_mod == 2:
        end_adj = 2

    adjusted_trimmed = trimmed_seqs[:, start_adj:len(str(trimmed_seqs[0].seq)) - end_adj]
    with open( args.outfile, "w") as output_handle:
        AlignIO.write(adjusted_trimmed, output_handle, args.outformat)

    print ("start adjust by: " + str(start_adj) + ", end adjusted by " + str(end_adj))


if __name__ == '__main__':
    main()
