import os
import random
import networkx as nx
import numpy as np
from collections import defaultdict


## THIS IS FOR TIME TRACKING PURPOSES ONLY
# Prints start time, total duration
import atexit
from time import time, strftime, localtime
from datetime import timedelta

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def log(s, elapsed=None):
    line = "="*40
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

start = time()
atexit.register(endlog)
log("Start Program")
## END OF TIME TRACKING METHOD



path = os.path.join(os.path.sep, "Users", "student", "Documents", "stats", "project", "localization")
directory = os.fsencode(path)

#create a list of all genes
# start with set of genes so we have all the unique ones
# then make a list so that order is preserved (for random selections)

supplement_path = os.path.join(os.path.sep, "Users", "student", "Documents", "stats", "project")
gene_set = set()
gene_dict = defaultdict(list)
with open(os.path.join(supplement_path, "srep-s3.txt")) as gene_file:
	for line in gene_file.readlines()[1:]:
		gene1 = line.strip().split()[0]
		gene2 = line.strip().split()[1]
		gene_set.add(line.strip().split()[0])  # 11117
		gene_set.add(line.strip().split()[1])  # 11029
		#TODO: fix number of genes: total is 13460, should be 10343??
		gene_dict[gene1].append(gene2)

genes = list(gene_set) # preserve order for true random selections

sizes = []
for key, val in gene_dict.items():
	sizes.append(len(val))
print(np.mean(sizes))

with open("lcc_zscores.txt", "w+") as outfile:
	outfile.write("tissue\tz_lcc\tlcc\tlcc_rand\tlcc_rand_std\n")

for file in os.listdir(directory):  # this iterates through all files in the directory
	filename = os.fsdecode(file)
	with open(os.path.join(path, filename)) as tissue_file:
		tissue_lines = tissue_file.readlines()  # reads file into memory

		tissue_lst = tissue_lines[1].strip().split()  # creates a list of all lines in the file

		#get the tissue file name (for the gene list)
		tissue = tissue_lst[-3][1:-2]

		#get the number of genes
		n = int(tissue_lst[-2])
		print(n)

		#extract the lcc
		lcc_lst = tissue_lines[2].strip().split()
		lcc = int(lcc_lst[-1])
		lcc_dist = []

		# now calculate the number of genes
		# select gene_count randomly
		for i in range (1, 1001):
			genes_rand = np.random.choice(genes, n, replace=True)

			# construct the graph
			G = nx.Graph()


			for node in genes_rand:
				if node in gene_dict:
					for j in gene_dict[node]:
						if j in genes_rand:
							G.add_edge(node, j)

			# record the lcc (calculate using networkx)
			if G.number_of_edges() == 0:
				lcc_rand = 0
			else:
				lcc_rand = len(max(nx.connected_components(G), key=len))
			lcc_dist.append(lcc_rand)

		mean_lcc = np.mean(lcc_dist)
		std_lcc = np.std(lcc_dist)

		z = (lcc - mean_lcc) / std_lcc
		print(str(n) + " " + str(z))
		with open("lcc_zscores.txt", "a") as outfile:
			outfile.write(tissue + "\t" + str(z) + "\t" + str(lcc) + "\t" + str(mean_lcc) + "\t" + str(std_lcc) + "\n")



