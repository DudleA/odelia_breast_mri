import pandas as pd
import os

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data'

df_annot = pd.read_excel(os.path.join(folder, 'ODELIA_annotations_USZ_31-03-25_studyuid.xlsx'), header=0, index_col=None)
df_key = pd.read_csv(os.path.join(folder, 'df_anon_key_total.csv'), header=0, index_col=0)
df_key = df_key.astype({'PHI-StudyDate': 'str'})
df_key['PHI-StudyYear'] = df_key['PHI-StudyDate'].str[:4]

for i in df_annot.index:
    if int(i) < 11:
        continue
    elif pd.notnull(df_annot.loc[i, 'StudyInstanceUID']):
        continue
    pid = df_annot.loc[i, 'Patient ID']
    pid = pid[4:]
    date = df_annot.loc[i, 'Date of Examination']
    date = date[:4]

    
    index_key = df_key.index[(df_key['ANON-PatientID'] == pid) & (df_key['PHI-StudyYear'] == date)]

    if len(index_key) == 1:
        df_annot.loc[i, 'StudyInstanceUID'] = df_key.loc[index_key[0], 'ANON-StudyUID']
    elif len(index_key) == 0:
        print("No match for", pid, date)
    else:
        print("Too many matches for", pid, date)
        print(index_key)

df_annot.to_excel(os.path.join(folder, 'ODELIA_annotations_USZ_31-03-25_studyuid.xlsx'))