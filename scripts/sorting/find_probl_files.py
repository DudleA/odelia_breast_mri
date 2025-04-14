import pandas as pd
import os
import numpy as np

"""Check if several studies have same StudyUID"""

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data'
df = pd.read_csv(os.path.join(folder, 'df_anon_key_total.csv'), header=0, index_col=0)

values, counts = np.unique(df['ANON-StudyUID'], return_counts=True)
for study in values[counts > 1][:2]:
    pid = df.loc[df['ANON-StudyUID'] == study, 'ANON-PatientID']
    if len(pid.unique()) > 1:
        print(pid)
        print(study)
