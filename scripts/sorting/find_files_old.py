import pandas as pd
import pydicom
import os
import shutil

"""
Missing: 
pid 008, dataset 015 -> missing in csv file, manually added
pid 102, dataset 015 -> missing in csv file, manually added
pid 170, dataset 015 -> missing in csv file, manually added
pid 200, dataset 015 -> missing in csv file, manually added
pid 201, dataset 015 -> second study missing in csv file, manually added
pid 221, dataset 015 -> missing in csv file, manually added
pid 229, dataset 015 -> missing in csv file, manually added
pid 238, dataset 015 -> missing in csv file, manually added
pid 244, dataset 015 -> missing in csv file, manually added
pid 250, dataset 015 -> missing in csv file, manually added
"""

folder_df = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Metadata_local_model'
# df_sorted = pd.read_csv(os.path.join(folder_df, 'clinical_data_USZ_2.csv'), header=0, index_col=0)
df_sorted = pd.read_excel(os.path.join(folder_df, 'annot_local_model.xlsx'), header=0, index_col=0)
df_mri_004 = pd.read_csv(os.path.join(folder_df, 'Dataset_004_DCE_DICOM_attributes_SUB_LATEST.csv'), header=0, index_col=0)
df_mri_015 = pd.read_csv(os.path.join(folder_df, 'Dataset_015_DCE_DICOM_attributes_SUB.csv'), header=0, index_col=0)

folder_img = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data'

for i in df_sorted.index:
    # pid = i[4:]
    pid = df_sorted.loc[i, 'ID'][4:]
    study_uid = df_sorted.loc[i, 'StudyInstanceUID']
    if os.path.exists(os.path.join(folder_img, 'Data_all/USZ/dicoms', pid, study_uid)):
        continue
    print(pid, study_uid)
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

        img_path = os.path.join(folder_img, 'Raw_data', subfolder, pid, study, 'Series-' + str(series), 'Image-1.dcm')
    
        if os.path.exists(img_path):
            print("Path exists")
            img = pydicom.dcmread(img_path)
            if study_uid == img.StudyInstanceUID:
                print("correct image found")
                output_path = os.path.join(folder_img, 'Data_all/USZ/dicoms', pid, study_uid)
                if not os.path.exists(os.path.join(folder_img, 'Data_all/USZ/dicoms', pid)):
                    os.mkdir(os.path.join(folder_img, 'Data_all/USZ/dicoms', pid))
                # if os.path.exists(output_path):
                #     shutil.rmtree(output_path)
                shutil.copytree(os.path.join(folder_img, 'Raw_data', subfolder, pid, study, 'Series-' + str(series)), 
                            os.path.join(output_path))
                image_found = True
                break
        else:
            print("Path not found")
        
    if not image_found:
        print("image not found: ", pid)


    