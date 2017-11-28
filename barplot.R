#read in data
expressed_genes = read.table("~/Desktop/BMI_Final/total_genes.txt", sep='') #table of total expressed genes in all tissues
localization = read.table("~/Desktop/BMI_Final/localization values", header=TRUE, sep='\t') #table of LCC size, module diameter, and LCC z score in all tissues

#create table including total expressed genes and localization data for filtering by significant LCC z-score
filter_data = cbind(localization[,1:2], localization[,4], expressed_genes, localization$diameter, localization$diameter*2000) #include diameter * 2000 for scaling on graph later
sig_tissue_data <- filter_data[filter_data$`localization[, 4]` >= 0.5,] #filter data by tissues w/ LCC z-score above 0.5
###this is not the same number of tissues given in the paper?

#plot the data
library(reshape2)
library(ggplot2)

plot = data.frame(tissue= sig_tissue_data$tissue.name, total_genes = sig_tissue_data$V1, LCC_size= sig_tissue_data$lcc.size, diameter=sig_tissue_data$`localization$diameter * 2000`)
plot.m = melt(plot, id.vars='tissue')

ggplot(plot.m, aes(tissue, value)) + 
  geom_bar(aes(fill = variable), width = 0.4, position = position_dodge(width=0.5), stat="identity") +  
  scale_fill_manual("Legend:", labels = c("total expressed genes", "largest connected component size", "module diameter"), values = c("black", "red", "blue")) +
  labs(y='Module size') +
  theme(legend.position="top",axis.text.x = element_text(angle = 90, hjust = 1),axis.title.x=element_blank()) +
  scale_y_continuous(sec.axis = sec_axis(~./2000, name='Module diameter')) #add secondary y axis
                                                                                                                                                
