import pandas as pd
import os
import glob
import pydicom

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data'

df_total = pd.DataFrame(columns=['ANON-PatientID', 'ANON-PatientName', 'PHI-PatientName', 'PHI-PatientID', 'DateOffset', 'PHI-StudyDate', 'ANON-AccNo', 'PHI-AccNo', 'ANON-StudyUID', 
                                'PHI-StudyUID', 'Series', 'Instances'])

for subfolder in ['PROJECT_004', 'PROJECT_004-b', 'PROJECT_004-c', 'PROJECT_004-d']:
    print(subfolder)
    df_path = glob.glob(os.path.join(folder, subfolder, 'private', 'phi_export', '100000_PROJECT_004*.csv'))
    df = pd.read_csv(df_path[0], header=0, index_col=None)
    df_total = pd.concat([df_total, df], ignore_index=True)
df_total.drop_duplicates(subset=['ANON-PatientID', 'PHI-PatientID', 'DateOffset', 'ANON-AccNo', 'ANON-StudyUID', 'PHI-StudyUID'], inplace=True, ignore_index=True)

for i in df_total.index:
    if 'xlfn.CONCAT' in df_total.loc[i, 'PHI-StudyUID']:
        df_total.loc[i, 'PHI-StudyUID'] = '1.2.840.113619.6.95.31.0.3.4.1.24.13.' + str(df_total.loc[i, 'PHI-AccNo'])

df_total.sort_values(by=['ANON-PatientID', 'PHI-StudyDate', 'ANON-AccNo'], inplace=True, ignore_index=True)


df_data_015 = pd.read_excel(os.path.join(folder, 'MRI_Breast_Dataset_015_Index_PHI_Name.xlsx'), header=0, index_col=0)
df_data_015.rename(columns={'ANON-Accession': 'ANON-AccNo', 'PHI-Accession': 'PHI-AccNo'}, inplace=True)
df_data_015.drop(columns=['FGT', 'BPE', 'Cancer BI-RADS', 'Comment'], inplace=True)

df_data_015['ANON-StudyUID'] = ""
df_data_015['PHI-StudyUID'] = '1.2.840.113619.6.95.31.0.3.4.1.24.13.' + df_data_015['PHI-AccNo'].astype(str)
df_data_015[['Series', 'Instances']] = 0
df_data_015['PHI-PatientName'] = df_data_015['ANON-PatientName']

print(df_data_015)

folder_img = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data/MRI_Breast_Dataset_015_ANON'
for i in df_data_015.index:
    pid = df_data_015.loc[i, 'ANON-PatientName']
    date = df_data_015.loc[i, 'ANON-StudyDate']
    print(pid, date)
    img_path = glob.glob(os.path.join(folder_img, pid, 'Study-MR-' + str(date) + '*', 'Series-2', 'Image-1.dcm'))
    if len(img_path) == 1:
        img_path = img_path[0]
    else:
        raise ValueError("Not right number of folders found:", img_path)
    img = pydicom.dcmread(img_path)
    df_data_015.loc[i, 'ANON-StudyUID'] = img.StudyInstanceUID


df_total = pd.concat([df_total, df_data_015], ignore_index=True)
df_total.sort_values(by=['ANON-PatientID', 'PHI-StudyDate', 'ANON-AccNo'], inplace=True, ignore_index=True)

df_total.to_csv(os.path.join(folder, 'df_anon_key_total.csv'))

