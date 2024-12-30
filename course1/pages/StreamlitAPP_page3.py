import numpy as np
import pandas as pd
import seaborn as sns
import random
from pathlib import Path
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
from views import Visualize
import geojson

#导入地图数据
with open(r'../data/geodata.json', encoding='utf-8') as f:
    geojson_data = geojson.load(f)


#设置plt字体
plt.rcParams['font.sans-serif'] = ['SimHei']

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
 )

#层级设置
page = st.sidebar.selectbox(
    '选择视图',
    (
        '2020年各地区人口年龄构成', 
        "2020年全国人口年龄构成",
        "2020年各地区人口",
        "2010/20年各地区分性别的人口数据"
    )
)

if page == '2020年各地区人口年龄构成':
    # 第二级菜单
    setting_option = st.sidebar.radio(
        "选择图片展示", 
        [
            "2020年各地区人口年龄构成柱状图"
        ]
    )

elif page == '2020年全国人口年龄构成':
    # 第二级菜单
    setting_option = st.sidebar.radio(
        "选择图片展示",
        [
            "2020年各地区人口年龄构成饼图",
            "2020年各地区人口年龄构成漏斗图"
        ]
    )
elif page == "2020年各地区人口":
    setting_option = st.sidebar.radio(
        "选择图片展示",
        [
            "2020年各地区人口直方图",
            "2020年各地区人口数量分布地图"
        ]
    )

else:
    setting_option = st.sidebar.radio(
        "选择图片展示",
        [
            "2010年-2020各地区人口数对比柱状图",
            "2020年各地区15岁及以上人口平均受教育年限柱状图"
        ]
    )

#导入数据1
data_region_age = pd.read_excel(r"../data/2020年各地区人口年龄构成.xlsx")
data_region_age['地区'] = data_region_age['地区'].str.replace(' ', '')

#导入数据2
df_age = pd.read_excel(r"..\data\2020年全国人口年龄构成.xlsx")
new_age_data = df_age.iloc[1:4]
new_age_data.sort_values(by = ['比例'], ascending = False, inplace = True, ignore_index = True)

#导入数据3
df_district = pd.read_excel(r"..\data\2020年各地区人口.xlsx")[1:]
df_district.sort_values(by = ["2020年占比", "2010年占比"], ascending=False, inplace=True)

#转换数据3
df_district_copy = df_district.copy()
df_district_copy.dropna(how = 'any', inplace = True) 

df_district_copy['人口数'] = df_district_copy['人口数'].astype('float64')
df_district_copy['地区'] = df_district_copy['地区'].apply(lambda x: x[0] + x[2] if x[1] == ' '  else x)

new_data = df_district_copy.iloc[:32,:]


#导入数据4
p2010 = pd.read_excel(r'..\data\2010年各地区分性别的人口数据.xlsx')
p2010 = p2010.iloc[1:,:]
p2010 = p2010.rename(columns = {'Unnamed: 0':'地区', '合计' : '2010人口数'})
p2010['地区'] = p2010['地区'].str.replace(' ', '')

new_data_copy = new_data.copy()
new_data_copy.rename(columns={'人口数': '2020人口数'}, inplace=True)
#表连接
df_2010_2020 = new_data_copy.merge(right = p2010, how = 'right', on = '地区')
df_2010_2020['2010人口数'] = df_2010_2020['2010人口数'].astype('float64')

df_2010_2020['10年增长数'] = df_2010_2020['2020人口数'] - df_2010_2020['2010人口数']
df_2010_2020.sort_values(by=['10年增长数'], inplace=True, ascending = False)

#导入数据5
df_edu_time = pd.read_excel(r"..\data\2020年各地区15岁及以上人口平均受教育年限.xlsx")

if __name__ == '__main__':

    if page == '2020年各地区人口年龄构成':

        if setting_option == "2020年各地区人口年龄构成柱状图":
            v = Visualize()
            st.title("2020年各地区人口年龄构成柱状图")
            
            fig1 = v.visualize_pdbarh(data_region_age)
            st.pyplot(fig1, use_container_width = False)
            
            #显示数据帧
            st.header('数据帧')
            st.dataframe(data_region_age, use_container_width = False, width = 1400, height = 600)

    elif page == '2020年全国人口年龄构成':
        
        if setting_option == "2020年各地区人口年龄构成饼图":
            v = Visualize()
            st.title("2020年各地区人口年龄构成饼图")
            fig2 = v.visualize_pie(
                new_age_data,
                values = '人数',
                names = '全国人口年龄构成',
                hole = 0.7,
            )
            col1, col2 = st.columns([1,3])

            col2.plotly_chart(fig2, use_container_width = True)

            #显示数据帧
            col1.dataframe(new_age_data, use_container_width = False, width = 400, height = 140)
        
        elif setting_option == "2020年各地区人口年龄构成漏斗图":
            v = Visualize()
            
            st.title("2020年各地区人口年龄构成漏斗图")
            fig3 = px.funnel_area(
                new_age_data,
                values = "比例",
                names = "全国人口年龄构成",
                color_discrete_sequence = px.colors.sequential.Agsunset,
                height = 800,
                width = 800,
                template = 'plotly_white'
            )
            col1, col2 = st.columns([1, 3])

            col2.plotly_chart(fig3, use_container_width = True )


            #显示数据帧
            col1.dataframe(new_age_data, use_container_width = False, width = 400, height = 140)
    elif page == '2020年各地区人口':
        
        if setting_option == "2020年各地区人口数量分布地图":
            v = Visualize()
            st.title("2020年各地区人口数量分布地图")
            
            fig4 = px.choropleth(
                new_data,
                geojson = geojson_data,
                locations = '地区',
                color = '人口数',
                featureidkey = 'properties.name',
                color_discrete_sequence = px.colors.sequential.amp,
                hover_data = ['人口数', '2020年占比', '2010年占比'],
                width = 1600,
                height = 1000
            )
            st.plotly_chart(fig4, use_container_width = False)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(new_data, use_container_width = False, width = 1400, height = 600)
        
        elif setting_option == "2020年各地区人口直方图":
            v = Visualize()
            st.title("2020年各地区直方图")
            fig5 = v.visualize_hist(
                df_district,
                x = '地区',
                y = ["2020年占比", "2010年占比"],
                barmode = 'group',
                ylabel = '百分比',
                legend = '占比'
            )
            st.plotly_chart(fig5, use_container_width = False)
            #显示数据帧
            st.header('数据帧')
            st.dataframe(data_region_age, use_container_width = False, width = 1400, height = 600)
    elif page == "2010/20年各地区分性别的人口数据":
        
        if setting_option == "2010年-2020各地区人口数对比柱状图":
            v = Visualize()
            st.title("2010年-2020各地区人口数对比柱状图")
            
            fig6 = v.visualize_bar(
                df_2010_2020,
                x = '地区',
                y = '10年增长数',
                color = '10年增长数',
                ylabel = '人口数',
                legend = '年份'
            )
            st.plotly_chart(fig6, use_container_width = False)
            
            #显示数据帧
            st.header('数据帧')
            st.dataframe(df_2010_2020, use_container_width = False, width = 1400, height = 600)

        elif setting_option == "2020年各地区15岁及以上人口平均受教育年限柱状图":
            v = Visualize()
            st.title("2020年各地区15岁及以上人口平均受教育年限柱状图")

            fig7 = v.visualize_bar(
                df_edu_time,
                x = '地区',
                y = ['2020年平均年限', '2010年平均年限'],
                ylabel = '平均受教育年限',
                legend = '年份'
            )

            st.plotly_chart(fig7, use_container_width = False)

            #显示数据帧
            st.header('数据帧')
            st.dataframe(df_edu_time, use_container_width = False, width = 1400, height = 600)
