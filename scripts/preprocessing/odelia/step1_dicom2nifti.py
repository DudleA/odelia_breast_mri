import pandas as pd
import os
import SimpleITK as sitk

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data'
# df = pd.read_csv(os.path.join(folder, 'Metadata_local_model', 'clinical_data_USZ_2.csv'), header=0, index_col=0)
# df = pd.read_excel(os.path.join(folder, 'Metadata_local_model', 'annot_local_model.xlsx'), header=0, index_col=0)
df = pd.read_csv('metadata_new_sub.csv', header=0, index_col=0)
# df = pd.read_csv('metadata_old_sub.csv', header=0, index_col=0)
print(len(df.index))
reader = sitk.ImageSeriesReader()

for i in df.index:

    pid = df.loc[i, 'PatientID']
    print(pid)
    study_uid = df.loc[i, 'StudyInstanceUID']
    series_uid = df.loc[i, 'SeriesInstanceUID']

    """Skip dicoms already processed"""
    if study_uid in os.listdir(os.path.join(folder, 'Data_all/USZ_1/data')):
        continue
    
    """For old downloaded dicoms"""
    # study = df.loc[i, 'Study']
    # series = df.loc[i, 'Series']
    # img_path = os.path.join(folder, 'Raw_data/MRI_Breast_Dataset_004_ANON', pid, study, series)
    # if not os.path.exists(img_path):
    #     img_path = os.path.join(folder, 'Raw_data/MRI_Breast_Dataset_015_ANON', pid, study, series)

    """For new dowloaded dicoms"""
    img_path = os.path.join(folder, 'Raw_data/Images', pid, study_uid, series_uid)
    if not os.path.exists(img_path):
        print("Image does not exist:", img_path)
        df.drop(labels=i, inplace=True)
    else:
        print(study_uid)
        dicom_names = reader.GetGDCMSeriesFileNames(img_path)
        reader.SetFileNames(dicom_names) 
        img_nii = reader.Execute()
        output_path = os.path.join(folder, 'Data_all/USZ_1/data', study_uid)

        if not os.path.exists(output_path):
            os.mkdir(output_path)
        else:
            raise ValueError("Output path already exists:", output_path)
        sitk.WriteImage(img_nii, os.path.join(output_path, 'Sub.nii.gz'))