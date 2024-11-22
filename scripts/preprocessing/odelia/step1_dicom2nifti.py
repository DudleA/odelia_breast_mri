# ------------------
# Add your code here
# -------------------
import pandas as pd
import os
# import pydicom
import SimpleITK as sitk

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data'
df = pd.read_csv(os.path.join(folder, 'Metadata_local_model', 'clinical_data_USZ_2.csv'), header=0, index_col=0)
print(len(df.index))
reader = sitk.ImageSeriesReader()

for i in df.index[2:]:
    pid = i[4:]
    study_uid = df.loc[i, 'StudyInstanceUID']
    img_path = os.path.join(folder, 'Data_selected', pid, study_uid)
    if not os.path.exists(img_path):
        df.drop(labels=i, inplace=True)
    # else:
    #     print(study_uid)
    #     dicom_names = reader.GetGDCMSeriesFileNames(img_path)
    #     reader.SetFileNames(dicom_names) 
    #     img_nii = reader.Execute()
    #     output_path = os.path.join(folder, 'Data_selected_nii', pid)
    #     if not os.path.exists(output_path):
    #         os.mkdir(output_path)
    #     sitk.WriteImage(img_nii, os.path.join(folder, 'Data_selected_nii', pid, 'sub.nii.gz'))


df = df[['Left side', 'Right side']]
df = df.sort_index()
df.to_csv(os.path.join(folder, 'Metadata_local_model', 'clinical_data_USZ_v2.csv'))
print(len(df.index))