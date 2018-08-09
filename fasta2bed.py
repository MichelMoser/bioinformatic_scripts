from Bio import SeqIO
from Bio.SeqIO.FastaIO import SimpleFastaParser


import sys
import argparse


import time

t0 = time.time()


parser = argparse.ArgumentParser(description='Convert fasta to bed.')

parser.add_argument('--input',type=str, help='fasta which gets converted')
parser.add_argument('--interval', type=int, default=10000000,  help='divide fasta into X Mbase-intervals')
parser.add_argument('--steps', type=int, default=0,  help='NOT implemented yet; will divide fasta into X intervals of equal size')
parser.add_argument('--prefix', type=str, default="interval",  help='prefix added to interval bed files')

args = parser.parse_args()

infile = args.input
print(infile)

totLength = 0


with open(infile) as handle: 
   fasta_list = [(name,len(seq)) for (name, seq) in  SimpleFastaParser(handle)]


cumsum = 0
name_list = []
file_counter = 0
if args.interval: 
	windowsize = args.interval
	for name, seqlen in fasta_list: 
		if cumsum < windowsize: 
			cumsum += seqlen
			name_list.append((name, seqlen))
		else: 
			file_counter += 1
			with open(args.prefix+str(file_counter)+".bed", "w") as outfile:
				for seq, seqlen in name_list: 
					outfile.write( "\t".join([seq,"0", str(seqlen)])+"\n")
			print(cumsum)
			cumsum = seqlen
			name_list = [(name, seqlen)]



t1 = time.time()

total = t1-t0
print(total)
