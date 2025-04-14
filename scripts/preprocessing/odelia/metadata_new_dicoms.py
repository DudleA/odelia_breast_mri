import pandas as pd
import numpy as np
import os
# import SimpleITK as sitk
import pydicom

df = pd.DataFrame(columns=['PatientID', 'Study', 'Series', 'SeriesNumber', 'SeriesDescription', 'StudyInstanceUID', 'SeriesInstanceUID', 'StudyDate',
                           'Rows', 'Columns', 'PixelSpacing', 'SliceThickness', 'MagneticFieldStrength', 'Manufacturer', 'ManufacturerModelName', 
                           'RepetitionTime', 'EchoTime', 'FlipAngle', 'SequenceType'])

folder = '/mnt/3aef1f67-f1f1-46a8-9ba1-1387521ef48d/Swarm_learning/Data/Raw_data/Images'

# counter = 0
# for pid in os.listdir(folder):
#     print(pid)
#     for study in os.listdir(os.path.join(folder, pid)):
#         print(study)
#         for series in os.listdir(os.path.join(folder, pid, study)):
#             df.loc[counter, ['PatientID', 'Study', 'Series']] = [pid, study, series]

#             dcm_path = os.path.join(folder, pid, study, series, os.listdir(os.path.join(folder, pid, study, series))[0])
#             img = pydicom.dcmread(dcm_path)
#             df.loc[counter, 'SeriesNumber'] = img.SeriesNumber
#             df.loc[counter, 'SeriesDescription'] = img.SeriesDescription
#             df.loc[counter, 'StudyInstanceUID'] = img.StudyInstanceUID
#             df.loc[counter, 'SeriesInstanceUID'] = img.SeriesInstanceUID
#             df.loc[counter, 'StudyDate'] = img.StudyDate
#             df.loc[counter, 'Rows'] = img.Rows
#             df.loc[counter, 'Columns'] = img.Columns
#             df.loc[counter, 'PixelSpacing'] = str(img.PixelSpacing)
#             df.loc[counter, 'SliceThickness'] = img.SliceThickness
#             try:
#                 df.loc[counter, 'MagneticFieldStrength'] = img.MagneticFieldStrength
#             except Exception:
#                 df.loc[counter, 'MagneticFieldStrength'] = ""
#             df.loc[counter, 'Manufacturer'] = img.Manufacturer
#             df.loc[counter, 'ManufacturerModelName'] = img.ManufacturerModelName
#             df.loc[counter, 'RepetitionTime'] = img.RepetitionTime
#             df.loc[counter, 'EchoTime'] = img.EchoTime
#             try:
#                 df.loc[counter, 'FlipAngle'] = img.FlipAngle
#             except Exception:
#                 df.loc[counter, 'FlipAngle'] = ""

#             if 'SUB' in df.loc[counter, 'SeriesDescription']:
#                 df.loc[counter, 'SequenceType'] = 'SUB'
#             elif (df.loc[counter, 'SeriesDescription'][0] == '(') & (df.loc[counter, 'SeriesDescription'][-1] == ')'):
#                 df.loc[counter, 'SequenceType'] = 'SUB'
#             elif (df.loc[counter, 'RepetitionTime'] > 1000) & (df.loc[counter, 'EchoTime'] > 50):
#                 df.loc[counter, 'SequenceType'] = 'T2'
#             elif (df.loc[counter, 'RepetitionTime'] < 10) & (df.loc[counter, 'EchoTime'] < 10):
#                 df.loc[counter, 'SequenceType'] = 'T1'
            
#             counter += 1

# df = df.sort_values(by=['PatientID', 'StudyDate', 'SeriesNumber'], ignore_index=True)
# print(df)
# df.to_csv('metadata_new_dicoms.csv')

df = pd.read_csv('metadata_new_dicoms.csv', index_col=0, header=0)

df = df[df['SequenceType'] == 'SUB']
"""Some studies don't have a subtraction sequence: not included"""

df = df.sort_values(by=['PatientID', 'StudyInstanceUID', 'SeriesNumber'])
df = df.groupby(by='StudyInstanceUID', as_index=False).first()

df = df.sort_values(by=['PatientID', 'StudyInstanceUID', 'SeriesNumber'])
# values, counts = np.unique(df['StudyInstanceUID'], return_counts=True)
# print(len(values[counts > 1]))

"""
Sort according to series number
groupby study instance, keep first
"""

df.to_csv('metadata_new_sub.csv')

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