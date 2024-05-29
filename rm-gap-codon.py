#!/usr/bin/env python3

import argparse
import subprocess
from Bio import AlignIO
import re

def get_args():
    parser = argparse.ArgumentParser(description="""Takes a nucleotide alignment of a coding region and trims out columnns that are all gaps if those columns represent one codon.""")
    parser.add_argument(
        'infile',
        type=str,
        help="""Name of the Alignment file"""
    )
    parser.add_argument(
        'outfile',
        type=str,
        help="""Name of the output file"""
    )
    parser.add_argument(
        '--informat',
        type=str,
        choices=["fasta","fastq","phylip","nexus","clustalw"],
        default="fasta",
        help="""Input format of the alignment (fasta, fastq, phylip, nexus, clustalw). Default: fasta"""
    )
    return parser.parse_args()

def main():
    args = get_args()

    align = AlignIO.read(args.infile,args.informat)
    length = align.get_alignment_length()

    trimal_selections=[]

    for i in range(0,length-1,3):
        pos1_no_gaps=re.sub(r'[?\-]','',align[: ,i])
        if len(pos1_no_gaps) == 0:
            pos2_no_gaps=re.sub(r'[?\-]','',align[: ,i+1])
            if len(pos2_no_gaps) == 0:
                pos3_no_gaps=re.sub(r'[?\-]','',align[: ,i+2])
                if len(pos3_no_gaps) == 0:
                    trimal_selections.append(str(i)+"-"+str(i+2))
    print(args.infile, len(trimal_selections))
    if trimal_selections:
        trimal_command="trimal -in %s -out %s -selectcols \{ %s \}" % (args.infile, args.outfile, ",".join(trimal_selections))
        # print(trimal_command)
        proc = subprocess.call(trimal_command,shell=True)
    else:
        copy_command="cp -a %s %s" % (args.infile, args.outfile)
        proc = subprocess.call(copy_command,shell=True)

if __name__ == '__main__':
    main()
