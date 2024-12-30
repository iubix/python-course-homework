import numpy as np
import pandas as pd
import seaborn as sns
import random
from pathlib import Path
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
import geojson
import matplotlib as mpl

mpl.rcParams['figure.facecolor'] = 'white'

with open(r'../data/geodata.json', encoding='utf-8') as f:
    geojson_data = geojson.load(f)

#数据可视化
class Visualize:

    #定义可视化函数
    def visualize_pdbar(self, df, num = 1):
        
        fig, ax = plt.subplots(figsize=(8, 6))
        #可视化数据1
        df_obj = df.plot(
            kind = 'bar',
            stacked = True,
            colormap = 'Set2',
            ax = ax
        )
        for c in df_obj.containers:
            labels = [f'{int(v.get_height())/num:.1f}%' if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels = labels, label_type = 'center', fontsize = 10, rotation = 90)


        plt.xticks(df.index, df['地区'].values, rotation = 45)
        plt.legend(bbox_to_anchor=(1,1.15), ncol = 10, facecolor = 'None', fontsize = 10)

        return fig

    def visualize_pdbarh(self, df, num = 1):
        fig, ax = plt.subplots(figsize=(8, 6))

        #可视化
        df_obj = df.plot(
            kind = 'barh',
            stacked = True,
            colormap = 'Set2',
            ax = ax
        )
        for c in df_obj.containers:
            labels = [f'{int(v.get_width())/num:.1f}%' if v.get_width() > 0 else '' for v in c]
            ax.bar_label(c, labels = labels, label_type = 'center', fontsize = 8)

        plt.yticks(df.index, df['地区'].values)
        plt.legend(bbox_to_anchor=(1,1.15), ncol = 10, facecolor = 'None', fontsize = 10)
        plt.ylabel('')
        
        return fig

    def visualize_hist(self, df, x, y, ylabel, barmode = 'relative', legend = 'variable'):

        fig = px.histogram(
            df,
            x = x,
            y = y,
            barmode = barmode,
            width = 1300, height = 1000,
            labels = {
                '地区': '地区',
                'variable': legend,
            },
        )
        fig.update_layout(
            yaxis_title = ylabel,
            xaxis = {
                'tickangle': 45
            }
        )
        return fig
    
    def trans_polardata(self, df):
        newedu_data = df.set_index(["地区"], inplace = False)

        columns = newedu_data.columns.values #iloc[0,:].index.to_list()
        values = newedu_data.values.sum(axis = 0)

        #新建表
        edu_new_df = pd.DataFrame(
            data = np.c_[values, columns],
            columns = ['人数', '学历']
        )
        #排序
        edu_new_df.sort_values(by = '人数', ascending = False, inplace = True)

        return edu_new_df
    
    def visualize_polar(self, df):

        #可视化
        fig = px.bar_polar(
            df, 
            r='人数',
            theta='学历',
            color='学历',
            template='plotly_dark',
            height = 800,
            width = 800,
        )
        #格式设置
        fig.update_layout(
            polar = {
                'angularaxis':{
                    'gridcolor' : 'rgb(255,255,255)',
                    'linecolor' :  'rgb(255,255,255)',
                    'showline' : False
                },
                'radialaxis':{
                    'gridcolor' : 'rgb(255,255,255)',
                    'linecolor' :  'rgb(255,255,255)',
                    'showline' : False,
                }
            }
        )
        return fig
    
    def visualize_pie(self, df, names, values, hole = 0.6):
        #可视化
        fig = px.pie(
            df,
            names = names,
            values = values,
            color_discrete_sequence = px.colors.sequential.RdBu,
            height = 1000,
            width = 1000,
            hole = hole,
            template = 'plotly_white'
        )
        return fig

    def visualize_bar(self, df, x, y, dir = 'v', color = None, barmode = 'relative', legend = 'variable', ylabel = 'Y'):
        fig = px.bar(
            df,
            x = x,
            y = y,
            barmode = barmode,
            orientation = dir,
            color = color,
            color_discrete_sequence = px.colors.sequential.RdBu,
            height = 800,
            width = 1400,
            template = 'plotly_dark',
            labels = {
                'variable' : legend
            }
        )
        fig.update_layout(
            yaxis_title = ylabel,
            xaxis = {
                'tickangle': 45
            }
        )
        return fig