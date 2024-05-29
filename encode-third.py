#!/usr/bin/env python3

from Bio import SeqIO, AlignIO

def main():
    seqs = AlignIO.read("0.99_lognorms-cutoff-mafft-nexus-min-70per-taxa-treeshrink.phy", "phylip-relaxed")
    for seq in seqs:
        encode_seq=""
        pos=1
        for seq_char in seq.seq:
            if (pos%3==0):
                if (seq_char.lower()=="a" or seq_char.lower()=="g"):
                    encode_seq+="R"
                elif (seq_char.lower()=="c" or seq_char.lower()=="t"):
                    encode_seq+="Y"
                else:
                    encode_seq+=seq_char
            else:
                encode_seq+=seq_char
            pos+=1
        seq.seq=encode_seq
    with open( "0.99_lognorms-cutoff-mafft-nexus-min-70per-taxa-treeshrink-RY-THIRD-POS.phy", "w") as output_handle:
        AlignIO.write(seqs, output_handle, "phylip-relaxed")

if __name__ == '__main__':
    main()

