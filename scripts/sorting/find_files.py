import pandas as pd
import pydicom
import os
import shutil

folder_df = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Metadata_local_model'
df_sorted = pd.read_csv(os.path.join(folder_df, 'clinical_data_USZ_2.csv'), header=0, index_col=0)
df_mri_004 = pd.read_csv(os.path.join(folder_df, 'Dataset_004_DCE_DICOM_attributes_SUB_LATEST.csv'), header=0, index_col=0)
df_mri_015 = pd.read_csv(os.path.join(folder_df, 'Dataset_015_DCE_DICOM_attributes_SUB.csv'), header=0, index_col=0)

folder_img = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data'

for i in df_sorted.index:
    print(i)
    pid = i[4:]
    if os.path.exists(os.path.join(folder_img, 'Data_selected', pid)):
        continue
    study_uid = df_sorted.loc[i, 'StudyInstanceUID']
    dataset = study_uid.split('.')[7]

    if dataset == '004':
        subset = df_mri_004[df_mri_004['PatientID'] == pid]
        subfolder = 'MRI_Breast_Dataset_004_ANON'
    elif dataset == '015':
        subset = df_mri_015[df_mri_015['PatientID'] == pid]
        subfolder = 'MRI_Breast_Dataset_015_ANON'
    else:
        raise ValueError("Dataset unknown:", dataset)
    
    # if len(subset) > 4:
    #     print("too many values:", subset)    
    if len(subset.index) == 0:
        print("no studies found: ", pid)
    
    list_studies = subset['Study'].unique()
    image_found = False
    for study in list_studies:
        series = subset.loc[subset['Study'] == study, 'SeriesNumber'].values
        series = series.min()

        img_path = os.path.join(folder_img, subfolder, pid, study, 'Series-' + str(series), 'Image-1.dcm')
    
        if os.path.exists(img_path):
            print("Path exists")
            img = pydicom.dcmread(img_path)
            if study_uid == img.StudyInstanceUID:
                print("correct image found")
                output_path = os.path.join(folder_img, 'Data_selected', pid, study_uid)
                if not os.path.exists(os.path.join(folder_img, 'Data_selected', pid)):
                    os.mkdir(os.path.join(folder_img, 'Data_selected', pid))
                shutil.copytree(os.path.join(folder_img, subfolder, pid, study, 'Series-' + str(series)), 
                            os.path.join(output_path))
                image_found = True
                break
        else:
            print("Path not found")
        
    if not image_found:
        print("image not found: ", pid)


    