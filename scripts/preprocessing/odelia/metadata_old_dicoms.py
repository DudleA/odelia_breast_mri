import pandas as pd
import numpy as np
import os
# import SimpleITK as sitk
import pydicom

df = pd.DataFrame(columns=['PatientID', 'Study', 'Series', 'SeriesNumber', 'SeriesDescription', 'StudyInstanceUID', 'SeriesInstanceUID', 'StudyDate',
                           'Rows', 'Columns', 'PixelSpacing', 'SliceThickness', 'MagneticFieldStrength', 'Manufacturer', 'ManufacturerModelName', 
                           'RepetitionTime', 'EchoTime', 'FlipAngle', 'SequenceType'])

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data'
counter = 0
for subfolder in ['MRI_Breast_Dataset_004_ANON', 'MRI_Breast_Dataset_015_ANON']:
    for pid in os.listdir(os.path.join(folder, subfolder)):
        print(pid)
        for study in os.listdir(os.path.join(folder, subfolder, pid)):
            print(study)
            for series in os.listdir(os.path.join(folder, subfolder, pid, study)):
                df.loc[counter, ['PatientID', 'Study', 'Series']] = [pid, study, series]

                dcm_path = os.path.join(folder, subfolder, pid, study, series, os.listdir(os.path.join(folder, subfolder, pid, study, series))[0])
                img = pydicom.dcmread(dcm_path)
                df.loc[counter, 'SeriesNumber'] = img.SeriesNumber
                df.loc[counter, 'SeriesDescription'] = img.SeriesDescription
                df.loc[counter, 'StudyInstanceUID'] = img.StudyInstanceUID
                df.loc[counter, 'SeriesInstanceUID'] = img.SeriesInstanceUID
                df.loc[counter, 'StudyDate'] = img.StudyDate
                df.loc[counter, 'Rows'] = img.Rows
                df.loc[counter, 'Columns'] = img.Columns
                try:
                    df.loc[counter, 'PixelSpacing'] = str(img.PixelSpacing)
                except Exception:
                    df.loc[counter, 'PixelSpacing'] = None

                for col in ['SliceThickness', 'MagneticFieldStrength', 'Manufacturer', 'ManufacturerModelName', 'RepetitionTime', 'EchoTime', 'FlipAngle']:
                    try:
                        df.loc[counter, col] = img.data_element(col).value
                    except Exception:
                        df.loc[counter, col] = None

                if 'SUB' in df.loc[counter, 'SeriesDescription']:
                    df.loc[counter, 'SequenceType'] = 'SUB'
                elif (df.loc[counter, 'SeriesDescription'][0] == '(') & (df.loc[counter, 'SeriesDescription'][-1] == ')'):
                    df.loc[counter, 'SequenceType'] = 'SUB'
                elif pd.notnull(df.loc[counter, 'RepetitionTime']) & pd.notnull(df.loc[counter, 'EchoTime']):
                    print(df.loc[counter, 'RepetitionTime'], df.loc[counter, 'EchoTime'])
                    if (int(df.loc[counter, 'RepetitionTime']) > 1000) & (int(df.loc[counter, 'EchoTime']) > 50):
                        df.loc[counter, 'SequenceType'] = 'T2'
                    elif (int(df.loc[counter, 'RepetitionTime']) < 10) & (int(df.loc[counter, 'EchoTime']) < 10):
                        df.loc[counter, 'SequenceType'] = 'T1'
                
                counter += 1

df = df.sort_values(by=['PatientID', 'StudyDate', 'SeriesNumber'], ignore_index=True)
print(df)
df.to_csv('metadata_old_dicoms.csv')

df = pd.read_csv('metadata_old_dicoms.csv', index_col=0, header=0)

df = df[df['SequenceType'] == 'SUB']
"""Some studies don't have a subtraction sequence: not included"""

"""
Sort according to series number
groupby study instance, keep first
"""
df = df.sort_values(by=['PatientID', 'StudyInstanceUID', 'SeriesNumber'], ignore_index=True)
df = df.groupby(by='StudyInstanceUID', as_index=False).first()

df = df.sort_values(by=['PatientID', 'StudyInstanceUID', 'SeriesNumber'], ignore_index=True)
# values, counts = np.unique(df['StudyInstanceUID'], return_counts=True)
# print(len(values[counts > 1]))

df.to_csv('metadata_old_sub.csv')

# print("Studies")
# for study in values[counts > 1][:2]:
#     pid = df.loc[df['StudyInstanceUID'] == study, 'PatientID']
#     if len(pid.unique()) > 1:
#         print(pid)
#         print(study)

# values, counts = np.unique(df['SeriesInstanceUID'], return_counts=True)
# print(values[counts > 1])

# print("Series")
# for series in values[counts > 1][:2]:
#     pid = df.loc[df['SeriesInstanceUID'] == series, 'PatientID']
#     study = df.loc[df['SeriesInstanceUID'] == series, 'StudyInstanceUID']
#     if len(pid.unique()) > 1:
#         print(pid)
#         print(study)
#         print(series)