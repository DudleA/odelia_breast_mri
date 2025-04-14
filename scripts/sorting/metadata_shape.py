import pandas as pd
import SimpleITK as sitk
import os

folder_img = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Data_selected/USZ/data'

list_patients = os.listdir(folder_img)
df_output = pd.DataFrame(columns=['Shape_X', 'Shape_Y', 'Shape_Z', 'Spacing_X', 'Spacing_Y', 'Spacing_Z'])
df_output.index.name = 'PatientID'

for patient in list_patients:
    img_path = os.path.join(folder_img, patient, 'sub.nii.gz')
    img = sitk.ReadImage(img_path)
    size_x, size_y, size_z = img.GetSize()
    dx, dy, dz = img.GetSpacing()
    patient = 'USZ-' + patient
    df_output.loc[patient, ['Shape_X', 'Shape_Y', 'Shape_Z']] = [size_x, size_y, size_z]
    df_output.loc[patient, ['Spacing_X', 'Spacing_Y', 'Spacing_Z']] = [dx, dy, dz]

df_output.sort_index(inplace=True)
print(df_output)

df_output.to_csv('metadata_shape_USZ.csv')