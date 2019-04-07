# -*- coding:UTF-8 -*-#
from Graph import *
from mainwindowUI import *
from pyecharts import Timeline
from PyQt5 import QtWidgets
import os
import sys

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()

    starbucks_df = read_data()
    starbucks_df_time = time_preprocessing(starbucks_df)
    # 转为json文件

    # 设置geo信息
    starbucks_world_geo = r'world.json'

    if not os.path.exists(r'Amount_Each_Country_Bar.html') or not os.path.exists(r'Amount_Each_Country_Pie.html'):
        # 国家数量统计
        df_con = group(starbucks_df, 'Country')
        df_con_index = count_by_group(df_con, True)
        df_con_index_ase = count_by_group(df_con, False)

        # 国家数量统计柱状图
        bar = bar_pic(df_con_index_ase, "Amount_Each_Country", 'Country', 'count')
        bar.render(r'Amount_Each_Country_Bar.html')
        pie = pie_pic(df_con_index, 'Amount_Each_Country', 'Country', 'count')
        pie.render(r'Amount_Each_Country_Pie.html')

    if not os.path.exists(r'fenbutu.html'):
        # 所有星巴克分布地图
        starbucks_category_color_stops = [['Starbucks', 'rgb(211,47,47)'], ]
        draw_map(starbucks_df, r'fenbutu.html')

    if not os.path.exists(r'Amount_in_Each_Timezone_Bar.html') or not os.path.exists(
            r'Amout_in_Each_Timezone_Pie.html'):
        # 时区数量统计
        df_time = group(starbucks_df_time, 'Time')
        df_time_index = count_by_group(df_time, True)
        df_time_index_ase = count_by_group(df_time, False)
        # 时区数量统计饼状图
        pie_time = pie_pic(df_time_index,'Amount of Starbucks in Each Timezone','Time','count')
        pie_time.render(r'Amout_in_Each_Timezone_Pie.html')

    if not os.path.exists(r'Amount_of_Country_in_Timezone_Pie.html'):
        # 时区内小时区的数量统计
        df_gp = group(starbucks_df_time, ['Time', 'Timezone'])
        df_gp.columns = ['count']
        df_index = group(starbucks_df_time, ['Time'])
        df_index = df_index.reset_index(drop=False)
        timeline = Timeline(is_auto_play=False, timeline_bottom=0)
        for i in range(df_index.shape[0]):
            string = df_index['Time'][i]
            df_a_time = df_gp['count'][string].to_frame()
            df_a_time = df_a_time.reset_index(drop=False)
            pie = pie_pic(df_a_time, 'Amount of Starbucks in ' + string, 'Timezone', 'count')
            timeline.add(pie, 'Amount of Starbucks in ' + string)
        timeline.render(r'Amount_of_Country_in_Timezone_Pie.html')

    if not os.path.exists(r'map_time.html'):
        df_time = group(starbucks_df_time, 'Time')
        df_time_index = count_by_group(df_time, True)

        # 按时区的所有星巴克分布地图
        starbucks_category_color_time = []
        timezone_amount = []
        for index in range(starbucks_df_time.shape[0]):
            i = df_time_index['count'][df_time_index.Time == starbucks_df_time['Time'][index]]
            timezone_amount.append(i)
        starbucks_df_time.insert(0, 'timezone_amount', timezone_amount)
        draw_timezone_map(starbucks_df_time, r'map_time.html')

    if not os.path.exists(r'distribution_map_country.html'):
        # 渐变图
        df_con = group(starbucks_df, 'Country')
        df_con_index = count_by_group(df_con, True)
        draw_distribution_map(starbucks_world_geo, df_con_index, 'Country', 'distribution_map_country.html')

    MainWindow.setupUi(MainWindow)
    MainWindow.setWindowTitle("星巴克数据分析工具")

    sys.exit(app.exec_())
