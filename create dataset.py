from Bio import SeqIO
import numpy as np
import pandas as pd


# 0. Definitions
def to_numpy(seqs):
    nucl_map = {"A": 0, "C": 1, "G": 2, "T": 3, # four nucleotides
                "Y": 4, "R": 4, "W": 4, "S": 4, "K": 4, "M": 4, # degenerate bases (2 bases represented)
                "D": 4, "V": 4, "H": 4, "B": 4, # degenerate bases (3 bases represented)
                "N": 4 } # ambigous nucleotide (4 bases represented)
    return np.vstack([
        np.array([nucl_map[ch] for ch in s], dtype=np.uint8) for s in seqs
    ])


def one_hot_encode(seq_array):
    n, length = seq_array.shape
    enc = np.vstack([np.eye(4), [0, 0, 0, 0]]).astype(np.uint8)
    return np.stack([enc[seq] for seq in seq_array], axis=0)


# 1. Link the sequences and phylum as the dictionary
#    1) Open the fasta file
filez = "sh_refs_qiime_ver9_99_29.11.2022.fasta"
dictionary1 = {}
# key of dictionary 1 (key1) = sequence, value of dictionary 1 (value1) = accession number of each sequence
for record in SeqIO.parse(filez, "fasta"):
    key, value = record.id, str(record.seq)
    dictionary1[value] = key

#    2) Open the text file
file_text = open('sh_taxonomy_qiime_ver9_99_29.11.2022.txt', 'r')
dictionary2 = {}
# key of dictionary 2 (key2) = accession number, value of dictionary 2 (value2) = phylum
lines = file_text.readlines()
for line in lines:
    seq_num = line.split()
    phylum = seq_num[1].split(';')
    phylum = phylum[1][3:]
    dictionary2[seq_num[0]] = phylum

#    3) Make the final dictionary - key: phylum, value: sequences
final = {}
for key1, value1 in dictionary1.items():# key1 = sequence, value1 = accession number
    value2 = dictionary2[value1]        # value2 = phylum
    if value2 in final:
        final[value2].append(key1)
    else:
        final[value2] = [key1]


# 3. Make the list of sequences of each phylum

# asco is the list containing the sequences of 'Ascomycota'
asco = final['Ascomycota']
# asco_seqs is the list containing the 400 <= length <= 600 sequences + adding 'N' to make the equal length (600)
asco_seqs = []
for seq in asco:
    if 500 <= len(seq) <= 650:
        if len(seq) != 650:
            seq += 'N' * (650 - len(seq))
        asco_seqs.append(seq)

asco_seqs_array = to_numpy(asco_seqs)
asco_seqs_array_encoded = one_hot_encode(asco_seqs_array)
np.save("asco_encoded.npy", asco_seqs_array_encoded)

# basi is the list containing the sequences of 'Basidiomycota'
basi = final['Basidiomycota']
# basi_seqs is the list containing the 400 <= length <= 600 sequences + adding 'N' to make the equal length (600)
basi_seqs = []
for seq in basi:
    if 500 <= len(seq) <= 650:
        if len(seq) != 650:
            seq += 'N' * (650 - len(seq))
        basi_seqs.append(seq)

basi_seqs_array = to_numpy(basi_seqs)
basi_seqs_array_encoded = one_hot_encode(basi_seqs_array)
np.save("basi_encoded.npy", basi_seqs_array_encoded)


