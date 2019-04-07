# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import pandas as pd

def read_data():
    data_url = 'starbucks.csv'
    df = pd.read_csv(data_url, header=0, encoding='UTF-8')
    df.columns = ['Brand', 'Store Number', 'Store Name', 'Ownership Type', 'Street Address', 'City', 'State/Province',
                  'Country', 'Postcode', 'Phone Number', 'Timezone', 'lon', 'lat','Average Score','Numofusers']

    df['lon'] = df['lon'].fillna(0)
    df['lat'] = df['lat'].fillna(0)
    # Convert Elevation series to float
    df['lon'] = df['lon'].astype(float)
    df['lat'] = df['lat'].astype(float)
    # Clean up by dropping null rows
    df = df.dropna(axis=1, how='all')
    df.fillna('', inplace=True)
    df = df.drop_duplicates('Store Number', keep="first", inplace=False)
    df = df.reset_index(drop=True)
    return df


def time_preprocessing(df):
    time = []
    timezone = []
    for i in range(df.shape[0]):
        arr = df['Timezone'][i].split(' ')
        if arr[0] == 'GMT+000000':
            arr[0] = 'GMT+0:00'
        if arr[0] == 'GMT+05:30':
            arr[0] = 'GMT+05:00'
        if arr[0] == 'GMT-03:30':
            arr[0] = 'GMT-03:00'
        timezone.append(' '.join(arr))
        time.append(arr[0])
    df = df.drop(['Timezone'], axis=1)
    df.insert(0, 'Time', time)
    df.insert(0, 'Timezone', timezone)
    return df


def group(df, a_list):
    df_gp = df.groupby(a_list).size()
    df_gp = df_gp.to_frame()
    return df_gp


def count_by_group(df_gp, asc):
    df_gp.columns = ['count']
    df_gp = df_gp.sort_values(by=['count'], ascending=asc)
    df_gp_index = df_gp.reset_index(drop=False)
    return df_gp_index


