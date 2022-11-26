# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 12:21:06 2022

@author: tasni
"""

import pandas as pd
import argparse

def get_range(age, start, end, inc = 5):
    u_lim = 0
    l_lim = 0
    while start < end:
        l_lim = start
        u_lim = start + (inc - 1)
        start = start + inc
        if age >= l_lim and age <= u_lim:
            break
        
    return l_lim, u_lim

def convert(in_file, sht_name, out_file):
    
    df = pd.read_excel(in_file, sheet_name = sht_name)
    
    disease = list(set(df['icd10']))
    
    df_nan = df[df['age'].isna()]
    
    df_nonan = df[df['age'].notna()]
    df_nonan['age'] = df_nonan['age'].str.replace(" years",'')
    df_nonan['age'] = df_nonan['age'].str.replace(" year",'')
    df_nonan.loc[df_nonan['age'].str.contains(' days'), 'age'] = '0'
    df_nonan.loc[df_nonan['age'].str.contains(' day'), 'age'] = '0'
    df_nonan.loc[df_nonan['age'].str.contains(' months'), 'age'] = '0'
    df_nonan.loc[df_nonan['age'].str.contains(' month'), 'age'] = '0'
    
    
    result = {}
    for d in disease:
        result[d] = {1: {}, 2:{}}
    
    
    for i, row in df_nonan.iterrows():
        if int(row['age']) == 0:
            try:
                result[row['icd10']][int(row['sex'])]['<1 Year'] += 1
            except KeyError:
                result[row['icd10']][int(row['sex'])]['<1 Year'] = 1
        elif int(row['age']) >= 1 and int(row['age']) <= 4:
            try:
                result[row['icd10']][int(row['sex'])]['1-4 Year'] += 1
            except KeyError:
                result[row['icd10']][int(row['sex'])]['1-4 Year'] = 1
    
        elif int(row['age']) >= 95:
            try:
                result[row['icd10']][int(row['sex'])]['95+ Year'] += 1
            except KeyError:
                result[row['icd10']][int(row['sex'])]['95+ Year'] = 1
    
        else:
            lower, upper = get_range(int(row['age']),5,94)
            key = str(lower)+'-'+str(upper)+' Year'
        
            try:
                result[row['icd10']][int(row['sex'])][key] += 1
            except KeyError:
                result[row['icd10']][int(row['sex'])][key] = 1                   
    
    for i, row in df_nan.iterrows():
        try:
            result[row['icd10']][row['sex']]['Uknown'] += 1
        except KeyError:
            result[row['icd10']][row['sex']]['Uknown'] = 1
            
    columns = ['<1 Year', '1-4 Year']
    
    for i in range(5, 94, 5):
        key = str(i) + '-' + str(i + 4) + ' Year'
        columns.append(key)
        
    columns.append('95+ Year')
    columns.append('Uknown')
            
    output_list = []
    for name, value in result.items():
        for sex in value.keys():
            i_list = []
            i_list.append(name)
            i_list.append(sex)
            
            for column in columns:
            
                try:
                    i_list.append(value[sex][column])
                except KeyError:
                    i_list.append(0)
                    
            output_list.append(i_list)
            
    columns.insert(0, 'Sex')
    columns.insert(0, 'Disease')
    
    df_converted = pd.DataFrame(output_list, columns = columns)
    df_converted.to_excel(out_file, index=False)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert VA Data")
    parser.add_argument('--input-file', type=str, required=True, help='Provide input file to convert')
    parser.add_argument('--sheet-name', type=str, required=True, help='Name of the sheet')
    parser.add_argument('--output-file', type=str, required=True, help='Provide output file name')

    args = parser.parse_args()
    input_file = args.input_file
    sheet_name = args.sheet_name
    output_file = args.output_file

    convert(input_file, sheet_name, output_file)
