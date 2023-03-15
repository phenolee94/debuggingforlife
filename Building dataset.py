# install biopython in python packages
from Bio import SeqIO

#download fasta files for Rozellomycota (https://doi.plutof.ut.ee/doi/10.15156/BIO/TH005184) and Glomeromycota (https://doi.plutof.ut.ee/doi/10.15156/BIO/TH005180)
#save fasta files to python, 5012 ITS from rozello, 984 ITS from glomero
fasta_rozello = "rozello.fasta"
fasta_glomero = "glomero.fasta"

#training dataset = 100 sequences of each
#test dataset = 600 sequences of each
training_set = []
test_set = []
count_rozello = 0
for record in SeqIO.parse(fasta_rozello, "fasta"):
    #print("Sequence ID:", record.id)
    #print("Sequence:", record.seq)
    if count_rozello < 100:
        training_set.append(record)
    elif count_rozello < 700:
        test_set.append(record)
    count_rozello += 1

count_glomero = 0
for record in SeqIO.parse(fasta_glomero, "fasta"):
    #print("Sequence ID:", record.id)
    #print("Sequence:", record.seq)
    if count_glomero < 100:
        training_set.append(record)
    elif count_glomero < 700:
        test_set.append(record)
    count_glomero += 1

#create training and test fasta files
SeqIO.write(training_set, "training_set.fasta", "fasta-2line")
SeqIO.write(test_set, "test_set.fasta", "fasta-2line")
