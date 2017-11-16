#read in data
exp_sig = read.table("/Users/capriarinaldi/Desktop/BMI_Final/Dataset2.txt", header=TRUE, sep='\t')
finalgenelist = read.table("/Users/capriarinaldi/Desktop/BMI_Final/finalgenelist.txt")

exp_sig2 = exp_sig[(exp_sig$gene_id %in% finalgenelist$V1),]

adipocyte = exp_sig2[,2] #choosing adipocyte column
print(adipocyte[1:5]) #check that you selected correct column
sig_adipocyte = which(adipocyte>1) #creating new array of only gene_id's with sig > 1
length(sig_adipocyte) #how many genes are in this array?

#simpler version combining code from above
sig_pfc = length(which(exp_sig2[,39]>1))
sig_pfc #testing the tissue they give a value for in the paper -- should be 2644 genes out of 10434


#for all tissues
sig_counts = NULL
for (i in 2:65){
  sig_counts[i]=length(which(exp_sig2[,i]>1))
}
sig_counts[39] #check the value for pfc

#bar plot of significant gene counts
barplot(sig_counts[2:65], 
        col = "darkgray", 
        xlab = "Tissue Type", ylab = "Total Expressed Genes", 
        ylim = c(0,5000),
        names.arg = names(exp_sig[2:65]), las=2, cex.names = 0.4)
