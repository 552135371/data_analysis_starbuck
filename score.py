# -*- coding: UTF-8 -*-


def input_score(df, score, name):
    for i in range(len(df)):
        if df['Store Name'][i] == name:
           df.loc[i, 'Average Score'] = average_score(df, i, score)
           df.loc[i, 'Numofusers'] += 1
           break
    return df


def average_score(df, i, score):
    sum = float(df.loc[i, 'Average Score'])*int(df.loc[i, 'Numofusers'])+score
    num = int(df.loc[i, 'Numofusers'])+1
    return sum/num

