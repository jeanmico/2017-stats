import os
import random

path = os.path.join(os.path.sep, "Users", "student", "Documents", "stats", "project", "localization")
directory = os.fsencode(path)

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	with open(os.path.join(path, filename)) as tissue_file:
		tissue_lines = tissue_file.readlines()

		tissue_lst = tissue_lines[1].strip().split()

		#get the tissue file name (for the gene list)
		tissue = tissue_lst[-3][1:-2]
		print(tissue)

		#get the number of genes
		n = int(tissue_lst[-2])
		print(n)

		#extract the lcc
		lcc_lst = tissue_lines[2].strip().split()
		lcc = int(lcc_lst[-1])


		# now calculate the number of genes
		n = 1
		genes = []
		# select gene_count randomly
		# for i in range (1, 1001):
		# 	random.sample(genes, n)

			# generate distribution



