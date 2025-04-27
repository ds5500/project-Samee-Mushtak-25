import pandas as pd

leu_df = pd.read_csv('Leu-vloop-stats-unique.csv')
ser_df = pd.read_csv('Ser-vloop-stats-unique.csv')

leu_seqs = leu_df['seq']
ser_seqs = ser_df['seq']

leu_seqs_set = set(leu_seqs)
ser_seqs_set = set(ser_seqs)
print(leu_seqs_set.intersection(ser_seqs_set))

