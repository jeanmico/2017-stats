import os
import random
import networkx as nx
import numpy as np

path = os.path.join(os.path.sep, "Users", "student", "Documents", "stats", "project", "localization")
directory = os.fsencode(path)

#create a list of all genes
# start with set of genes so we have all the unique ones
# then make a list so that order is preserved (for random selections)

supplement_path = os.path.join(os.path.sep, "Users", "student", "Documents", "stats", "project")
gene_set = set()
gene_inter = []
with open(os.path.join(supplement_path, "srep-s3.txt")) as gene_file:
	for line in gene_file.readlines()[1:]:
		gene_set.add(line.strip().split()[0])  # 11117
		gene_set.add(line.strip().split()[1])  # 11029
		#TODO: fix number of genes: total is 13460, should be 10343??
		gene_inter.append([line.strip().split()[0], line.strip().split()[1]])
print(len(gene_inter))
genes = list(gene_set) # preserve order for true random selections

with open("lcc_zscores.txt", "w+") as outfile:
	outfile.write("tissue\tz_lcc\tlcc\tlcc_rand\tlcc_rand_std\n")

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	with open(os.path.join(path, filename)) as tissue_file:
		tissue_lines = tissue_file.readlines()

		tissue_lst = tissue_lines[1].strip().split()

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
		for i in range (1, 500):
			genes_rand = random.sample(genes, n)

			# construct the graph
			G = nx.Graph()

			#list search is slow and sparse
			#to speed this up, execute a grep/awk
			# for i in gene_inter:
			# 	if i[0] in genes_rand and i[1] in genes_rand:
			# 		G.add_edge(i[0], i[1])
			result = [x for x in gene_inter if x[0] in genes_rand and x[1] in genes_rand]
			for x in result:
				G.add_edge(x[0], x[1])
			# record the lcc (calculate using networkx)
			if G.number_of_edges() ==0:
				lcc_rand = 0
			else:
				lcc_rand = len(max(nx.connected_components(G), key=len))
			lcc_dist.append(lcc_rand)

		mean_lcc = np.mean(lcc_dist)
		std_lcc = np.std(lcc_dist)

		z = (lcc - mean_lcc) / std_lcc

		with open("lcc_zscores.txt", "a") as outfile:
			outfile.write(tissue + "\t" + str(z) + "\t" + str(lcc) + "\t" + str(mean_lcc) + "\t" + str(std_lcc) + "\n")



