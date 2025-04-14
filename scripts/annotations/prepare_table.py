import pandas as pd
import os
import numpy as np

def interpet_annot(v, b):

    b = b[b != 'not provided']
    b = b.astype(int)
    if ('Invasive Cancer (no special type)' in v) | ('Invasive Cancer (lobular carcinoma)' in v) | ('Invasive Cancer (all other)' in v):
        return 'Malignant lesion'
    elif 'DCIS' in v:
        return 'DCIS'
    elif 'Benign lesion' in v:
        return 'Benign lesion'
    elif len(b) > 0:
        if np.max(b) <= 3:
            return 'Benign lesion'
        else:
            return 'not provided'
    else:
        return 'not provided'


folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Data_all/USZ_1/metadata'
df_full = pd.read_excel(os.path.join(folder, 'annotation.xlsx'), header=0, index_col=0)
df_full = df_full.dropna(subset=['StudyInstanceUID'])

df_output = pd.DataFrame(columns=['ID', 'StudyInstanceUID', 'Left side', 'Right side', 'Indication'])

list_pids = df_full['Patient ID'].unique()
print(len(list_pids))

list_study_uid = df_full['StudyInstanceUID'].unique()
print(len(list_study_uid))

counter = 0

for study_uid in list_study_uid:
    # print(study_uid)
    subset = df_full[df_full['StudyInstanceUID'] == study_uid]
    pid = subset['Patient ID'].values[0]
    side = subset['Side']
    df_output.loc[counter, 'ID'] = pid
    df_output.loc[counter, 'StudyInstanceUID'] = study_uid
    indication = subset['Indication '].values[0]
    df_output.loc[counter, 'Indication'] = indication

    if ('left' in side.values) & ('right' in side.values):
        lesion_type = subset.loc[subset['Side'] == 'left', 'Type of Lesion']
        birads = subset.loc[subset['Side'] == 'left', 'BIRADS']
        df_output.loc[counter, 'Left side'] = interpet_annot(lesion_type.values, birads.values)

        lesion_type = subset.loc[subset['Side'] == 'right', 'Type of Lesion']
        birads = subset.loc[subset['Side'] == 'right', 'BIRADS']
        df_output.loc[counter, 'Right side'] = interpet_annot(lesion_type.values, birads.values)

    elif 'right' in side.values:
        lesion_type = subset.loc[subset['Side'] == 'right', 'Type of Lesion']
        birads = subset.loc[subset['Side'] == 'right', 'BIRADS']

        df_output.loc[counter, 'Left side'] = 'No lesion'
        df_output.loc[counter, 'Right side'] = interpet_annot(lesion_type.values, birads.values)

    elif 'left' in side.values:
        lesion_type = subset.loc[subset['Side'] == 'left', 'Type of Lesion']
        birads = subset.loc[subset['Side'] == 'left', 'BIRADS']

        df_output.loc[counter, 'Left side'] = interpet_annot(lesion_type.values, birads.values)
        df_output.loc[counter, 'Right side'] = 'No lesion'
    
    else:
        df_output.loc[counter, 'Left side'] = 'No lesion'
        df_output.loc[counter, 'Right side'] = 'No lesion'

    counter += 1

df_output = df_output[df_output['Left side'] != 'not provided']
df_output = df_output[df_output['Right side'] != 'not provided']

print(df_output)
df_output.to_excel(os.path.join(folder, 'annot_local_model.xlsx'))