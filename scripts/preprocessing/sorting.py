import pandas as pd
import os
import shutil
import numpy as np
import glob
import pydicom

meta_folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Metadata_local_model'
df_annot = pd.read_excel(os.path.join(meta_folder, 'annot_local_model.xlsx'), header=0, index_col=0)
df_mri_004 = pd.read_csv(os.path.join(meta_folder, 'Dataset_004_DCE_DICOM_attributes_SUB_LATEST.csv'), header=0, index_col=0)
df_mri_015 = pd.read_csv(os.path.join(meta_folder, 'Dataset_015_DCE_DICOM_attributes_SUB.csv'), header=0, index_col=0)

print(len(df_annot.index))
df_annot = df_annot[df_annot['Indication'] != 'Follow up']
df_annot = df_annot[df_annot['Indication'] != 'Evaluation of the effect of neoadjuvant chemotherapy']

df_annot['Left side int'] = df_annot['Left side'].apply(lambda x: {'No lesion': 0, 'Benign lesion': 1, 'DCIS': 2, 'Malignant lesion': 3}[x])
df_annot['Right side int'] = df_annot['Right side'].apply(lambda x: {'No lesion': 0, 'Benign lesion': 1, 'DCIS': 2, 'Malignant lesion': 3}[x])
df_annot['Max side int'] = np.maximum(df_annot['Left side int'], df_annot['Right side int'])
print(len(df_annot.index))

"""Remove duplicates of same patient"""
list_ids = df_annot.loc[df_annot['Max side int'] > 1, 'ID'].values
list_ids = list(list_ids)

df_annot.sort_values(by=['Max side int'], inplace=True, ascending=False, ignore_index=True)
counter_1 = 0
counter_0 = 0
for i in df_annot.index:
    pid = df_annot.loc[i, 'ID']
    if df_annot.loc[i, 'Max side int'] > 1:
        continue
    elif pid in list_ids:
        df_annot = df_annot.drop(labels=i)
    elif (df_annot.loc[i, 'Max side int'] == 1) & (counter_1 < 45):
        list_ids.append(pid)
        counter_1 += 1
    elif (df_annot.loc[i, 'Max side int'] == 0) & (counter_0 < 42):
        list_ids.append(pid)
        counter_0 += 1
    else:
        df_annot = df_annot.drop(labels=i)

print(len(df_annot.index))  
values, counts = np.unique(df_annot['Max side int'], return_counts=True)
print("Distribution")
print(values)
print(counts)

# df_annot = df_annot[['ID', 'Left side', 'Right side']]
df_annot = df_annot.set_index('ID')
print(df_annot)
df_annot.to_csv(os.path.join(meta_folder, 'clinical_data_USZ_2.csv'))


# img_folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data'

# for i in df_annot.index[:5]:
#     pid = df_annot.loc[i, 'ID'][4:]
#     print('\n', pid)
#     study_uid = df_annot.loc[i, 'StudyInstanceUID']
#     print(study_uid)

#     indices_004 = df_mri_004.index[df_mri_004['PatientID'] == pid]
#     for j in indices_004:
#         series = df_mri_004.loc[j, 'Series']
#         study = df_mri_004.loc[j, 'Study']
#         input_path = os.path.join(img_folder, 'MRI_Breast_Dataset_004_ANON', pid, study, series)
#         if os.path.exists(input_path):
            
#             """Check study instance uid"""
#             img = pydicom.dcmread(os.path.join(input_path, 'Image-1.dcm'))
#             if img.StudyInstanceUID == study_uid:
#                 print(series, study)
#                 """Choose correct series (several substration images??)"""
#                 """Copy"""
#         else:
#             print("Image not found:", pid, study, series)

#     indices_015 = df_mri_015.index[df_mri_015['PatientID'] == pid]
#     for j in indices_015:
#         series = df_mri_015.loc[j, 'Series']
#         study = df_mri_015.loc[j, 'Study']
#         input_path = os.path.join(img_folder, 'MRI_Breast_Dataset_015_ANON', pid, study, series)
#         if os.path.exists(input_path):

#             """Check study instance uid"""
#             img = pydicom.dcmread(os.path.join(input_path, 'Image-1.dcm'))
#             if img.StudyInstanceUID == study_uid:
#                 print(series, study)
#                 """Choose correct series"""
#                 """Copy"""

#         else:
#             print("Image not found:", pid, study, series)
    
